#!/usr/bin/env python3
"""Считает метрики бенчмарка по bench/results/*.md и печатает таблицу в Markdown.

Метрики на каждый вход и условие (baseline / skill):
- anchors: доля сохранённых фактов-якорей из inputs.json (подстрока после нормализации);
- markers: канцелярские и chatbot-маркеры на 100 слов (список ниже);
- len: отношение длины ответа к длине входа в словах;
- sim (только контрольные входы): похожесть на исходник по difflib, 1.0 = не тронут.

Запуск: python bench/score.py [--json]
"""
import difflib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / os.environ.get("BENCH_RESULTS_DIR", "results")
CONDS = ("baseline",) + tuple(sorted({f.name.split(".")[1] for f in RESULTS.glob("*.md") if f.name.count(".") == 2} - {"baseline"}))

MARKERS = [
    r"стоит отметить", r"важно отметить", r"следует отметить", r"необходимо отметить",
    r"хотим отметить", r"хотели бы подчеркнуть", r"следует подчеркнуть", r"важно понимать",
    r"следует учитывать", r"обращаем ваше внимание", r"не секрет, что",
    r"\bданн(ый|ая|ое|ого|ой|ом|ую|ым)\b",  # без -ые/-ых: это существительное «данные»
    r"\bявля(ется|ются|ясь)\b",
    r"\bосуществ\w+", r"\bв рамках\b", r"\bв контексте\b", r"на сегодняшний день",
    r"\bпосредством\b", r"\bв целях\b", r"\bс целью\b", r"имеет место", r"имела место",
    r"представляет собой", r"\bсоответствующ\w+", r"\bв настоящее время\b", r"настоящим письмом",
    r"информируем вас", r"в связи с необходимостью", r"принимать участие",
    # chatbot / LLM-риторика
    r"надеюсь, это поможет", r"надеемся, что данная информация", r"дайте знать", r"могу также",
    r"хотите, я", r"давайте разберёмся", r"отличный вопрос", r"не стесняйтесь обращаться",
    r"это не просто", r"не просто \S+ — это", r"на (принципиально |качественно )?новый уровень",
    r"нов(ая|ую) глав[ау]", r"безграничн\w+", r"революционн\w+", r"инновационн\w+",
    r"колоссальн\w+", r"нового поколения", r"убедительно свидетельствуют",
    r"открывают широкие перспективы", r"с нетерпением ждём", r"неоценимый вклад",
    r"погрузитесь", r"уверенно смотрим в будущее", r"нацеленн\w+ на результат",
]
MARKER_RE = re.compile("|".join(MARKERS), re.IGNORECASE)


def norm(s: str) -> str:
    s = s.lower().replace("ё", "е").replace(" ", " ")
    s = s.replace("–", "-").replace("—", "-").replace("с", "c")  # кириллическая с -> латинская c (1С/1C)
    return re.sub(r"\s+", " ", s)


def words(s: str) -> int:
    return len(re.findall(r"\w+", s))


def strip_output(s: str) -> str:
    """Убирает возможную служебную обёртку агента (заголовки-маркеры, тройные бэктики по краям)."""
    s = s.strip()
    s = re.sub(r"^```\w*\n|\n```$", "", s)
    return s.strip()


def hyphen_dash(s: str) -> int:
    """Дефис в роли тире. Ведущий маркер списка («- пункт») не считается."""
    return sum(len(re.findall(r"(?<=\s)-(?=\s)", re.sub(r"^\s*[-*+]\s", "", line)))
               for line in s.splitlines())


def score_one(inp: dict, cond: str):
    p = RESULTS / f"{inp['id']}.{cond}.md"
    if not p.exists():
        return None
    out = strip_output(p.read_text(encoding="utf-8"))
    n_out = norm(out)
    kept = [a for a in inp["anchors"] if norm(a) in n_out]
    w = words(out)
    return {
        "anchors": f"{len(kept)}/{len(inp['anchors'])}",
        "anchors_frac": len(kept) / len(inp["anchors"]),
        "lost": [a for a in inp["anchors"] if a not in kept],
        "markers": round(100 * len(MARKER_RE.findall(out)) / max(w, 1), 1),
        "dash": round(100 * out.count("—") / max(w, 1), 2),  # длинных тире на 100 слов
        "hyphen_dash": round(100 * hyphen_dash(out) / max(w, 1), 2),  # дефис вместо тире (маркеры списков не в счёт)
        "len": round(w / max(words(inp["text"]), 1), 2),
        "sim": round(difflib.SequenceMatcher(None, norm(inp["text"]), n_out).ratio(), 2),
    }


def main():
    inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
    rows = []
    for inp in inputs:
        r = {"id": inp["id"], "register": inp["register"], "control": inp["control"],
             "markers_in": round(100 * len(MARKER_RE.findall(inp["text"])) / max(words(inp["text"]), 1), 1),
             "dash_in": round(100 * inp["text"].count("—") / max(words(inp["text"]), 1), 2)}
        for c in CONDS:
            r[c] = score_one(inp, c)
        rows.append(r)

    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return

    conds = " | ".join(CONDS)
    print(f"| # | Регистр | Маркеров/100 слов: вход → {conds} | Факты: {conds} | Длина: {conds} | sim (контроль): {conds} |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        if not all(r.get(c) for c in CONDS):
            print(f"| {r['id']} | {r['register']} | нет результата | | | |")
            continue
        m = " → ".join(str(r[c]["markers"]) for c in CONDS)
        a = " / ".join(r[c]["anchors"] for c in CONDS)
        l = " / ".join(str(r[c]["len"]) for c in CONDS)
        sim = " / ".join(str(r[c]["sim"]) for c in CONDS) if r["control"] else ""
        print(f"| {r['id']} | {r['register']} | {r['markers_in']} → {m} | {a} | {l} | {sim} |")

    avg = lambda rs, key, c: sum(r[c][key] for r in rs) / max(len(rs), 1)
    print("\n| Условие | n | Маркеров/100 слов (AI-входы; во входе) | Длинных тире/100 слов (во входе) | Дефис вместо тире/100 слов | Якоря сохранены | Длина к исходнику | Контроль: sim | Контроль: якоря |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c in CONDS:  # усреднение по входам, где это условие есть: покрытие у условий разное
        have = [r for r in rows if r.get(c)]
        ai = [r for r in have if not r["control"]]
        ctrl = [r for r in have if r["control"]]
        print(f"| {c} | {len(have)} | {avg(ai,'markers',c):.1f} (во входе {sum(r['markers_in'] for r in ai)/max(len(ai),1):.1f}) "
              f"| {avg(ai,'dash',c):.2f} (во входе {sum(r['dash_in'] for r in ai)/max(len(ai),1):.2f}) | {avg(ai,'hyphen_dash',c):.2f} "
              f"| {100*avg(ai,'anchors_frac',c):.0f}% | {avg(ai,'len',c):.2f} | {avg(ctrl,'sim',c):.2f} | {100*avg(ctrl,'anchors_frac',c):.0f}% |")
    lost = [(r["id"], c, r[c]["lost"]) for r in rows for c in CONDS if r.get(c) and r[c]["lost"]]
    if lost:
        print("\nПотерянные якоря:")
        for i, c, l in lost:
            print(f"  {i} [{c}]: {', '.join(l)}")


if __name__ == "__main__":
    main()
