#!/usr/bin/env python3
"""Слепая парная оценка baseline vs skill.

  python bench/judge.py make [seed] -> bench/judge/pairs-<n>.md (ослеплённые пары для судьи) + bench/judge/key.json
  python bench/judge.py report  -> читает bench/judge/verdicts-*.json, снимает ослепление, печатает итог

Судья получает исходник, запрос и два варианта A/B в случайном порядке и отвечает JSON-ом:
{"id": ..., "winner": "A"|"B"|"tie", "facts_lost": {"A": [...], "B": [...]}, "facts_invented": {"A": [...], "B": [...]}, "why": "..."}
"""
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent
COND = os.environ.get("BENCH_COND", "skill")  # какое условие сравниваем с baseline
JD = ROOT / os.environ.get("BENCH_JUDGE_DIR", "judge" if COND == "skill" else f"judge-{COND}")
PER_FILE = int(os.environ.get("BENCH_PER_FILE", "5"))
RESULTS = ROOT / os.environ.get("BENCH_RESULTS_DIR", "results")


def make():
    JD.mkdir(exist_ok=True)
    inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20260906)  # python judge.py make <seed>
    key, chunks = {}, []
    for inp in inputs:
        outs = {}
        for c in ("baseline", COND):
            p = RESULTS / f"{inp['id']}.{c}.md"
            if not p.exists():
                break
            outs[c] = p.read_text(encoding="utf-8").strip()
        if len(outs) < 2:
            continue
        a_is_skill = rng.random() < 0.5
        key[inp["id"]] = {"A": COND if a_is_skill else "baseline", "B": "baseline" if a_is_skill else COND}
        a, b = (outs[COND], outs["baseline"]) if a_is_skill else (outs["baseline"], outs[COND])
        chunks.append(
            f"## {inp['id']}\n\n**Регистр:** {inp['register']}\n\n**Запрос пользователя:** {inp['prompt']}\n\n"
            f"**{'Исходные данные' if inp.get('kind') in ('generate', 'voice') else 'Исходный текст'}:**\n\n{inp['text']}\n\n"
            f"**Вариант A:**\n\n{a}\n\n**Вариант B:**\n\n{b}\n"
        )
    (JD / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    for i in range(0, len(chunks), PER_FILE):
        (JD / f"pairs-{i // PER_FILE + 1}.md").write_text("\n---\n\n".join(chunks[i:i + PER_FILE]), encoding="utf-8")
    print(f"{len(chunks)} пар, файлов pairs-*.md: {(len(chunks) + PER_FILE - 1) // PER_FILE}")


def report():
    key = json.loads((JD / "key.json").read_text(encoding="utf-8"))
    inputs = {i["id"]: i for i in json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))}
    verdicts = []
    for p in sorted(JD.glob("verdicts-*.json")):
        verdicts += json.loads(p.read_text(encoding="utf-8"))
    wins = {COND: 0, "baseline": 0, "tie": 0}
    rows = []
    for v in verdicts:
        k = key[v["id"]]
        w = "tie" if v["winner"] == "tie" else k[v["winner"]]
        wins[w] += 1
        lost = {k[s]: v.get("facts_lost", {}).get(s, []) for s in ("A", "B")}
        lost = {("skill" if kk == COND else kk): vv for kk, vv in lost.items()}
        inv = {k[s]: v.get("facts_invented", {}).get(s, []) for s in ("A", "B")}
        inv = {("skill" if kk == COND else kk): vv for kk, vv in inv.items()}
        rows.append((v["id"], inputs[v["id"]]["register"], w, lost, inv, v.get("why", ""), inputs[v["id"]].get("kind", "rewrite")))
    print(f"| # | Регистр | Лучше | Потеряно фактов (baseline / {COND}) | Выдумано (baseline / {COND}) | Комментарий судьи |")
    print("|---|---|---|---|---|---|")
    for i, reg, w, lost, inv, why, kind in rows:
        f = lambda d: f"{len(d['baseline'])} / {len(d['skill'])}"
        print(f"| {i} | {reg} ({kind}) | {w} | {f(lost)} | {f(inv)} | {why} |")
    n = len(rows)
    order = ["rewrite", "subtle", "long", "generate", "voice", "control"]
    kinds = sorted({r[6] for r in rows}, key=order.index)
    if len(kinds) > 1:
        print(f"\n| Тип входов | n | {COND} / baseline / ничья | Потеряно (baseline / {COND}) | Выдумано (baseline / {COND}) |")
        print("|---|---|---|---|---|")
        for k in kinds:
            rs = [r for r in rows if r[6] == k]
            c = lambda w: sum(1 for r in rs if r[2] == w)
            print(f"| {k} | {len(rs)} | {c(COND)} / {c('baseline')} / {c('tie')} "
                  f"| {sum(len(r[3]['baseline']) for r in rs)} / {sum(len(r[3]['skill']) for r in rs)} "
                  f"| {sum(len(r[4]['baseline']) for r in rs)} / {sum(len(r[4]['skill']) for r in rs)} |")
    print(f"\nИтого (n={n}): {COND} {wins[COND]}, baseline {wins['baseline']}, ничья {wins['tie']}")
    for c in ("baseline", "skill"):  # в lost/inv условие всегда лежит под ключом "skill"
        print(f"{COND if c == 'skill' else c}: потеряно фактов {sum(len(r[3][c]) for r in rows)}, выдумано {sum(len(r[4][c]) for r in rows)}")


if __name__ == "__main__":
    {"make": make, "report": report}[sys.argv[1]]()
