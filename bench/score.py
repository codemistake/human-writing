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
CONDS = ("baseline", "skill")

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


def score_one(inp: dict, cond: str):
    p = ROOT / os.environ.get("BENCH_RESULTS_DIR", "results") / f"{inp['id']}.{cond}.md"
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
        "len": round(w / max(words(inp["text"]), 1), 2),
        "sim": round(difflib.SequenceMatcher(None, norm(inp["text"]), n_out).ratio(), 2),
    }


def main():
    inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
    rows = []
    for inp in inputs:
        r = {"id": inp["id"], "register": inp["register"], "control": inp["control"],
             "markers_in": round(100 * len(MARKER_RE.findall(inp["text"])) / max(words(inp["text"]), 1), 1)}
        for c in CONDS:
            r[c] = score_one(inp, c)
        rows.append(r)

    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return

    print("| # | Регистр | Маркеров/100 слов: вход → baseline → skill | Факты: baseline / skill | Длина: baseline / skill |")
    print("|---|---|---|---|---|")
    for r in rows:
        b, s = r["baseline"], r["skill"]
        if not (b and s):
            print(f"| {r['id']} | {r['register']} | нет результата | | |")
            continue
        extra = f" | sim {b['sim']} / {s['sim']}" if r["control"] else ""
        print(f"| {r['id']} | {r['register']} | {r['markers_in']} → {b['markers']} → {s['markers']} "
              f"| {b['anchors']} / {s['anchors']} | {b['len']} / {s['len']}{extra} |")

    done = [r for r in rows if r["baseline"] and r["skill"]]
    ai = [r for r in done if not r["control"]]
    ctrl = [r for r in done if r["control"]]
    if ai:
        avg = lambda key, c: sum(r[c][key] for r in ai) / len(ai)
        print(f"\nAI-входы (n={len(ai)}): маркеров/100 слов вход {sum(r['markers_in'] for r in ai)/len(ai):.1f}, "
              f"baseline {avg('markers','baseline'):.1f}, skill {avg('markers','skill'):.1f}; "
              f"факты сохранены baseline {100*avg('anchors_frac','baseline'):.0f}%, skill {100*avg('anchors_frac','skill'):.0f}%; "
              f"длина baseline {avg('len','baseline'):.2f}, skill {avg('len','skill'):.2f}")
    if ctrl:
        avg = lambda key, c: sum(r[c][key] for r in ctrl) / len(ctrl)
        print(f"Контроль (n={len(ctrl)}): похожесть на исходник baseline {avg('sim','baseline'):.2f}, skill {avg('sim','skill'):.2f}; "
              f"факты baseline {100*avg('anchors_frac','baseline'):.0f}%, skill {100*avg('anchors_frac','skill'):.0f}%")
    lost = [(r["id"], c, r[c]["lost"]) for r in done for c in CONDS if r[c]["lost"]]
    if lost:
        print("\nПотерянные якоря:")
        for i, c, l in lost:
            print(f"  {i} [{c}]: {', '.join(l)}")


if __name__ == "__main__":
    main()
