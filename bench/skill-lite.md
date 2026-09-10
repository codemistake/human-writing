---
name: human-writing
description: "Russian-first writing skill for natural reader-facing prose. Use when drafting, rewriting, polishing, or reviewing messages, documentation, posts, emails, explanations, reports, release notes, UI copy, or other text meant for people. Prefer Russian rules for Russian text and English rules for English text. Also use when the user asks to make text sound natural, less robotic, less formal, less AI-like, remove bureaucratic language, or match their voice. Do not use to change code semantics, fabricate facts, or add fake personal experience."
license: MIT
metadata:
  version: 1.3.1-lite
  language: ru-primary-en-secondary
---

# Human Writing

Пиши так, как пишет компетентный человек для другого человека. Основной язык этого скилла — русский; английский поддерживается как второй язык.

Цель — не «обмануть AI-детектор». Цель — убрать типичные дефолты LLM: пустые вводные, канцелярит, одинаковый ритм, псевдоглубину, избыточную структуру, сервисный тон и искусственную гладкость.

## 0. Ядро

Если помнишь только это, помни это. Остальные разделы уточняют ядро, но не отменяют его.

1. Каждое утверждение в результате должно быть в исходнике или в данных пользователя. Не можешь показать, откуда оно, — удали.
2. Числа, даты, имена, названия, условия, отрицания и причины переносятся целиком. «Обращения снизились на 12%» нельзя превратить в «выручка выросла на 12%».
3. Режь воду, а не содержание: призыв к действию, просьба, благодарность, квантор («все»), причина, обращение и подпись — содержание.
4. Хороший текст не трогай. Если запрос «проверь», а править нечего, верни как есть.
5. Не выдумывай «естественность»: ни опечаток, ни сленга, ни мнений, ни деталей ради живости.
6. Регистр жанра важнее правил стиля: договор остаётся договором, научная аннотация — научной, инструкция — шагами с командами в коде.
7. Голос автора из образца копируется на уровне формы (пунктуация, время глаголов, связки), а не фактов.
8. Длинный текст после правки перечитай целиком: нет ли дублей и ссылок на вырезанное.

