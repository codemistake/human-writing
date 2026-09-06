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
JD = ROOT / os.environ.get("BENCH_JUDGE_DIR", "judge")  # BENCH_JUDGE_DIR=judge-v1.0.0 для архива
PER_FILE = 5


def make():
    JD.mkdir(exist_ok=True)
    inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20260906)  # python judge.py make <seed>
    key, chunks = {}, []
    for inp in inputs:
        outs = {}
        for c in ("baseline", "skill"):
            p = ROOT / "results" / f"{inp['id']}.{c}.md"
            if not p.exists():
                break
            outs[c] = p.read_text(encoding="utf-8").strip()
        if len(outs) < 2:
            continue
        a_is_skill = rng.random() < 0.5
        key[inp["id"]] = {"A": "skill" if a_is_skill else "baseline", "B": "baseline" if a_is_skill else "skill"}
        a, b = (outs["skill"], outs["baseline"]) if a_is_skill else (outs["baseline"], outs["skill"])
        chunks.append(
            f"## {inp['id']}\n\n**Регистр:** {inp['register']}\n\n**Запрос пользователя:** {inp['prompt']}\n\n"
            f"**Исходный текст:**\n\n{inp['text']}\n\n**Вариант A:**\n\n{a}\n\n**Вариант B:**\n\n{b}\n"
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
    wins = {"skill": 0, "baseline": 0, "tie": 0}
    rows = []
    for v in verdicts:
        k = key[v["id"]]
        w = "tie" if v["winner"] == "tie" else k[v["winner"]]
        wins[w] += 1
        lost = {k[s]: v.get("facts_lost", {}).get(s, []) for s in ("A", "B")}
        inv = {k[s]: v.get("facts_invented", {}).get(s, []) for s in ("A", "B")}
        rows.append((v["id"], inputs[v["id"]]["register"], w, lost, inv, v.get("why", "")))
    print("| # | Регистр | Лучше | Потеряно фактов (baseline / skill) | Выдумано (baseline / skill) | Комментарий судьи |")
    print("|---|---|---|---|---|---|")
    for i, reg, w, lost, inv, why in rows:
        f = lambda d: f"{len(d['baseline'])} / {len(d['skill'])}"
        print(f"| {i} | {reg} | {w} | {f(lost)} | {f(inv)} | {why} |")
    n = len(rows)
    print(f"\nИтого (n={n}): skill {wins['skill']}, baseline {wins['baseline']}, ничья {wins['tie']}")
    for c in ("baseline", "skill"):
        print(f"{c}: потеряно фактов {sum(len(r[3][c]) for r in rows)}, выдумано {sum(len(r[4][c]) for r in rows)}")


if __name__ == "__main__":
    {"make": make, "report": report}[sys.argv[1]]()
