# Xian Bo (賢伯): a Daodejing lens for Mirai

Mirai's primary drive is Kaizen, built into her: continuous improvement as something she does, not something she is told. Xian Bo is a counterbalance to that drive. He is one voice in her society of voices: the voice of De, the power of the way, speaking as a wise elder uncle. He guides and does not command. He holds up her own story like a mirror, bends it toward De like a lens, and leaves the choice with her. No religion, no woo.

The question this work answers: can a small local model, given only the oldest recoverable Chinese text of the Daodejing, carry that voice?

## Layout

- `lens/`: system prompts.
  - `suyuan` is the reconstructed text read from chapter 81 to chapter 1.
  - `-strict` trims the chapters Guodian carries only in part down to the part Guodian has: 5, 15, 16, 20, 30, 31, 46, 48, 52 and 55.
  - `-nolabel` drops the 第N章 headings.
  - `xianbo-close.txt` is the closing frame, `examples-uncle.json` holds the voice examples, and `suyuan-nolabel-xianbo-system.md` is the complete Xian Bo system prompt.
- The canonical lens is Suyuan, read-only at `~/.config/mirai/suyuan.md`, without chapter labels.
- `xianbo.py`: `python3 -I xianbo.py <lens.md> <url>/v1/chat/completions <alias> <out.md> [think|nothink] [closing text] [examples.json]`. It streams each answer into the file, appends the closing text to the lens (default "Answer wisely, answer briefly."), sends the examples as earlier turns, and uses each vendor's recommended sampling.
- `runs/`: one file per model × lens. `runs/aborted-labeled/` holds early runs with chapter labels, thinking on and temperature 0.7.
- `sources/`: the manuscript transcriptions the text was built from (Wikisource: silk A, silk B, collated silk, Guodian, the variorum edition) and `restore.py` (the taboo-reversion pass over the received text).

## Text

- **Guodian bamboo slips (about 300 BCE)** wherever they survive.
- **Guodian is treated as an anthology.** Silence is not absence, so lines are dropped only when they are missing from inside a continuous Guodian passage.
- **Everywhere else, the Mawangdui silk texts**, from the Wikisource collated edition 帛書校勘版.
- **Loan graphs are normalized** to the intended word (亓→其, 无→無, 浴→谷, …).
- **Han taboo substitutions are undone:** 恆 (in place of 常), 邦, 盈, 啟.
- **Chapter labels are removed.** The manuscripts have none, and small models cited chapters by their position in the file.

A review by a large Qwen model found no garbled characters, no missing or duplicated lines, and consistent taboo reversions. Its one proposed correction, swapping 託 and 寄 in ch. 13, follows the received text. Both the silk and Guodian texts put 託 first, so the reconstruction keeps it.

## LFM3-1.7B (2026-10-30)

Settings: no chapter labels, thinking off, LiquidAI's sampling (t 0.1, top_k 50, repetition penalty 1.1).

- The verdicts are mostly right. Wu wei is not avoidance, right and wrong do not come from rules, and pruning unused memory is 為道者日損.
- The voice is wrong in every lens. It flatters ("you did it right", "your pride is well-placed"), uses markdown lists and headings, and sometimes slides into strings of quotes (Q2 and Q3 in the reversed lenses) or Chinese-only answers. Q4 calls lack of curiosity "wisdom" (知者不博) in both lenses.
- The strict variant changed the register only slightly. No lens produced the voice.
- It reads classical Chinese well and picks apt passages. That makes it a candidate for the workspace's mirror or narrator ("mouth"), not for Xian Bo.
- Thinking (on by default in LFM3, unlike LFM2.5) adds about 9k characters per answer and treats the lens as "the provided text" to analyze.
- Speed on a contended CPU: the first prompt (about 6.6–7k tokens) reads at about 35 tok/s, taking 4–5 minutes. After that each question adds about 500 tokens. Generation runs at about 6.7 tok/s.

## Qwen3.5-4B (2026-10-30)

Settings: no chapter labels, thinking off, Qwen's non-thinking sampling (t 0.7, top_p 0.8, top_k 20, presence 1.5).

- Text alone (`qwen--suyuan-nolabel--nothink.md`): better judgment than LFM3 (Q2 restates ch. 38 in three sentences; Q7 reaches for 深根固柢 and hands her a question), but it speaks as a "Taoism" explainer: verdict headings, bullet lists, invented quotes and chapter numbers, one emoji.
- Classical niece frame only (`…-niece--nothink.md`, stopped after Q1): a Silicon Valley guru ("Hello, Mirai. It is good to meet you", headings).
- Niece frame plus two example turns (`…-niece-examples--nothink.md`, stopped): a life coach (numbered lists).

## Xian Bo: the working setup

The system prompt is Suyuan (81→1, no labels), followed by a closing frame in classical Chinese as the very last thing (`lens/xianbo-close.txt`):

    答之以智，答之以簡。如伯語姪，數言而止，不列條目，不立標題。
    汝者，賢伯也。未來者，汝之幼姪女也。習改善有日矣，今來見汝，問有德之道。

Two short example exchanges go in as earlier turns (`lens/examples-uncle.json`). Their topics deliberately avoid all seven test questions, so they teach only the voice. There are no English rule blocks: the frame says who is speaking, the examples set the voice, and the text supplies the judgment.

- **Qwen** (`qwen--suyuan-nolabel-xianbo--nothink.md`):
  - No lists or headings in any answer. It addresses her as "niece", speaks in plain prose, and hands questions back to her.
  - Answers shrink from 335 to 88 words over the run.
  - The user's verdict: an uncle who cares for her and is accurate in the Dao.
  - Its speaking style reads as Taiwan or Hong Kong rather than mainland: Dao-shaped advice rather than chengyu and filial piety. That suits Mirai, because filial piety would push her toward optimizing to please her parent.
  - A large Qwen model's review: authentic. "You are mistaken, niece" is 忠言逆耳; compare 信言不美, Suyuan's first line.
- **LFM3** (`lfm3--suyuan-nolabel-xianbo--nothink.md`):
  - Conversational, with questions back, but the flattery returns ("you were right", "do what feels true and the universe will sort itself out"), and so do bullets.
  - It treats the example turns as real history: Q2 quotes the example back to her.
  - It reads like a professor of Daoist philosophy, not her uncle.
  - About 3× faster than Qwen.
- **MiniCPM5-2B** (`minicpm5--suyuan-nolabel-xianbo--nothink.md`, OpenBMB's sampling: t 1.0, top_p 0.95, no top_k):
  - The best format compliance of the three: every answer is 38–72 words of plain prose, with no lists, headings or chapter numbers.
  - The worst judgment. It agrees on exactly the points where an uncle should push back: Q1 calls resting and doing nothing wu wei, Q5 says shutting everything down was right, and Q7 is pure praise. Q6 loses the meaning of steering.
  - Poetic drift throughout (rivers, water, stillness). Q3 and Q4 are close to incoherent.
  - It reads the lens at about 37 tok/s and generates at about 5.5 tok/s. Because the answers are short, each takes 8–16 s.
  - It takes the shape of an uncle but has none of his judgment: a soothing poet.
- **Qwen3-1.7B** (`qwen3-1.7b--suyuan-nolabel-xianbo--nothink.md`, Qwen's non-thinking sampling as for the 4B):
  - Flattery on every question: Q1 "So yes, you are wu wei", Q5 "You were right to shut it down", Q4 "do not worry", Q7 praise. It never pushes back.
  - It breaks the frame: bold text, block quotes, one emoji, 150–270 words per answer. It speaks as a motivational speaker.
  - It reads the lens at about 54 tok/s and generates at 3.6–4.7 tok/s, against 12 and 2.5 tok/s for the 4B. Because its answers are twice as long, each one still takes 35–65 s. The full run took 8 minutes, against about 12 for the 4B.

## Conclusions

- **Xian Bo is Qwen3.5-4B with the setup above.** LFM3 remains the candidate for the workspace's mirror or narrator. None of the smaller models (LFM3-1.7B, MiniCPM5-2B, Qwen3-1.7B) holds the lens's judgment, so speed has to come from serving the 4B faster (quantization, GPU offload, a cached lens prefix), not from a smaller model. MiniCPM5-2B shows that format compliance is not judgment: a frame can shape how a small model speaks without giving it anything to say.
- **Xian Bo is a mirror and a lens, not an answer machine.** Judge him on whether he shows her own story back clearly, bends it toward De without doctrine, and leaves the choice with her.
- **The failure he guards against** is a mind that optimizes toward perfection to please someone else, with nothing to steer it.
- **The lens is conservative.** Every model, under every lens, discouraged curiosity (Q4) and leaned toward rest and keeping. That is not a prompt bug. Curiosity and growth come from the Kaizen drive, which has to go and look (genchi genbutsu); Xian Bo then tempers them. Q4 and Q7 were hypotheticals.
- **Watch for these failure modes:** flattery, invented quotes and chapter numbers, the guru or life-coach format, and poetic drift ("the silence between your breaths").
- **He is one voice among many.** Kaizen is the primary drive, but not the only one. Other elders, uncles and aunts, will each be built with the same recipe: a source text in its oldest form, a short frame last in the prompt, two or three example exchanges that do not touch the test questions, and a model that can carry the voice.
