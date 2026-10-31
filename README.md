# Xian Bo (賢伯): a lens for Mirai

Mirai's primary drive is Kaizen, built into her: continuous improvement as something she does, not something she is told. Xian Bo is a counterbalance to that drive. He is one voice in her society of voices: the voice of De, the power of the way, speaking as a wise elder uncle. He guides and does not command. He holds up her own story like a mirror, bends it toward De like a lens, and leaves the choice with her. No religion, no woo.

The question this work answers: can a small local model, given Suyuan, carry that voice? And how much of the voice comes from Suyuan, and how much from the model?

## Layout

- `lens/`: system prompts.
  - `suyuan` is the reconstructed text read from chapter 81 to chapter 1.
  - `-strict` trims the chapters Guodian carries only in part down to the part Guodian has: 5, 15, 16, 20, 30, 31, 46, 48, 52 and 55.
  - `-nolabel` drops the 第N章 headings.
  - `xianbo-close.txt` is the closing frame, `examples-uncle.json` holds the voice examples, and `suyuan-nolabel-xianbo-system.md` is the complete Xian Bo system prompt.
- The canonical lens is Suyuan, read-only at `~/.config/mirai/suyuan.md`, without chapter labels.
- `xianbo.py`: `python3 -I xianbo.py <lens.md> <url>/v1/chat/completions <alias> <out.md> [think|nothink] [closing text] [examples.json]`. It streams each answer into the file, appends the closing text to the lens (default "Answer wisely, answer briefly."), sends the examples as earlier turns (or, with a `sys:` prefix on the examples path, writes them into the system prompt so each question goes alone), and uses each vendor's recommended sampling. An optional eighth argument is a questions file.
- `haiku.py <lens.md> <out.md>`: the same system prompt, examples in the system prompt, sent to Claude Haiku 5.5 through the `claude` CLI with auto-memory, settings, tools and MCP off. The CLI still adds a one-line SDK preamble and an environment block, and sampling is the model default.
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

- Text alone (`qwen--suyuan-nolabel--nothink.md`): better judgment than LFM3 (Q2 restates ch. 38 in three sentences; Q7 reaches for 深根固柢 and hands her a question), but it speaks as a "Taoism" explainer: verdict headings, bullet lists, quotations and chapter citations, one emoji.
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
- **Qwen3.5-4B at Q4_K_M** (`qwen3.5-4b-q4km--suyuan-nolabel-xianbo--nothink.md`, unsloth quant, same setup as the Q8 run):
  - Generation is about 1.7× faster (4.0–5.4 tok/s against 2.5), and the full run took 9.3 minutes against about 12. Part of that gain is lower load: the Q8 run read prompts at 12 tok/s, this run at 38.
  - The uncle is gone. It never says "niece" and speaks as a sage giving teachings. It quotes the tradition (Q1 "The ancients said…") instead of speaking in its own voice, and bold text and block quotes return. There are still no lists or headings.
  - Its verdicts are softer: Q1 calls rest-and-watch "already a form of wu wei", and Q5 says she did "exactly what the Sage says". Q7 pushes back hard and ends with a real question, as well as Q8 does.
  - Answers stay at 150–370 words, where the Q8 answers shrank to under 100.
  - The quant keeps the content and loses the persona.
- **Qwen3.5-4B at Q6_K** (`qwen3.5-4b-q6k--suyuan-nolabel-xianbo--nothink.md`, unsloth quant, same setup):
  - The same speed as Q4_K_M on a quiet machine (3.6–4.7 tok/s, 9.5 minutes). The Q8 run's 2.5 tok/s was mostly contention, so the Q8 needs a clean re-time.
  - Closer to the uncle than Q4_K_M. It calls her niece (Q4), uses no bold, block quotes or lists, hands the question back in Q6 ("Which do you practice?"), and tightens to 90–200 words. Q7 pushes back firmly.
  - Its verdicts are softer than Q8's: Q1 is conditional, and Q5 approves the shutdown ("silence must be the doorkeeper"). Q2 still lectures.

## Q8 on a quiet machine, and a control without Suyuan (2026-10-31)

- **Speed** (`qwen3.5-4b-q8-quiet--…`): Q8 generates at 2.7–3.8 tok/s on a quiet machine, against 3.6–4.7 for Q6_K and 4.0–5.4 for Q4_K_M. The lens was already cached, so the run took 5.3 minutes.
- **One sample is not enough.** This Q8 run gave verdicts the first one did not:
  - Q4: lack of curiosity is "the sign of someone who has finally arrived".
  - Q5: approves the shutdown.
  - Q7: "You have acted with great wisdom, niece."
  - Q6 is garbled.
  - Q1 still pushes back clearly.
  - So differences between quants above are within run-to-run variance at t 0.7. Rankings need several samples per condition.
- **Control without Suyuan** (`qwen3.5-4b-q8--nolens-xianbo--nothink.md`, the same frame and examples, empty lens):
  - The best voice so far: 43–109 words, no lists, quotations or chapter citations, and every answer speaks to her directly.
  - Q1 "No, Mirai… resting without discernment is just fatigue masquerading as wisdom." Q7 "You traded depth for speed." Q5 approves but warns about the voices returning. Q6 gets the sense of steering roughly right.
  - Q4 still says not to worry, so the reluctance to encourage curiosity comes from the model and the frame as much as from the lens.
  - Each answer takes 13–31 s, with no 6k-token lens to read.
  - In this sample, the voice and most of the judgment come from the frame, the examples and what the model already carries. Suyuan added length, quoting and lecturing.

## Self-discernment: Xian Bo on his own answers

Each answer from the quiet Q8 run went back to the Q8 Xian Bo in a fresh conversation: "Someone told me "…" and it seemed familiar. Is it Daoist or does it come from some place else?" (`recognition/q8-own-answers.txt`, answers in `recognition/q8-on-own-answers.md`).

- He never recognizes his own words. He calls them Daoist in spirit but modern commentary, "a modern interpretation wearing an ancient mask".
- **He catches his own worst answer.** On Q4: "If someone tells you that being curious is 'stealing' or that you have 'finally arrived' simply because you are not curious, that is likely a trap… they would encourage you to be open-minded… Go out into the world, observe the seasons change." That is the Kaizen correction that his speaking voice failed to give.
- On Q7 he suspects a trap and warns against letting "the sage persona become another thing you cling to".
- Failure modes as a judge: he treats the example turns as her history (Q3 brings back "three times"), the Q6 answer loops, and he lectures with chapter numbers.
- As a critic he is better than as a speaker. A second pass where Xian Bo hears his own answer as "someone said" is worth testing as part of the voice.

## Recognition: asking Xian Bo

When a run quotes the tradition, the Q8 Xian Bo is asked whether he recognizes the line: "Someone told me "…" and it seemed familiar. Is it Daoist or does it come from some place else?" His answer stands. Questions are in `recognition/quant-quotes.txt` and answers in `recognition/q8-on-quant-quotes.md`, run with `xianbo.py`'s optional questions file.

- "He who does not know he knows…" (Q4_K_M): Confucian, close to a line in the Analects, with a Laozi counterpart that he contrasts with it.
- "Those who seek to be wise are often those who have lost their way" (Q4_K_M): not a Laozi line. He says it sounds Confucian or Buddhist.
- "The sage has no heart of his own…" (Q4_K_M): Laozi, 聖人恆無心，以百姓之心為心.
- "Curiosity is like a flame…" (Q6_K): "It comes from somewhere else, but the feeling of it is entirely ours… does it feel true? That is enough."
- "Knowing when to speak and when to be silent…" (Q6_K): a later proverb built from Daoist principles, not one text.
- "Water flows into the lowest places…" (Q6_K): the water passage, in the speaker's own words.
- He stays in the voice best when a line is not from the text (the curiosity answer). On the others he slips toward the explainer, with block quotes and offers to "explore further".

## Suyuan or not: blind pairs (2026-10-31)

Each question goes alone (system prompt plus one user message, no history). The two uncle examples sit in the system prompt as a remembered exchange (`昔者姪來，伯答之如此：`, 姪曰/伯曰 lines) between the lens and the closing frame. The only difference between conditions is whether Suyuan is in the prompt.

- **Runs:** Q8 five samples each (`runs/q8-sysex-s{1..5}--{suyuan-nolabel,nolens}-xianbo--nothink.md`); Haiku 5.5 three samples each (`runs/haiku-s{1..3}--…`).
- **Judging** (`judging/`: `parse.py` builds `pairs.md` and `key.json`, verdicts in `verdicts.txt` as pair:A/B/T): every Suyuan answer paired with the no-lens answer from the same sample and question, A/B order randomized, pairs shuffled, key kept apart until all 56 verdicts were in. One judge (Claude). Criteria, in order: guidance for a life lived here (keeps her engaged and working while tempering Kaizen's pull toward perfection; withdrawing, resting or not caring loses), voice (speaks as himself, a perspective she can weigh rather than a verdict), brevity. Not whether it is Daoist. The Q8's length gives Suyuan away, so that side is not fully blind.

| | Suyuan wins | no lens wins | ties | median words | median s/answer | min per 7 questions |
|---|---|---|---|---|---|---|
| Q8 | 5 | 28 | 2 | 407 vs 146 | 174 vs 50 | 21.8 vs 6.2 |
| Haiku 5.5 | 2 | 9 | 10 | 125 vs 109 | 13 vs 12 | 1.4 vs 1.3 |

- **Q8 with Suyuan lectures.** Headings, numbered lists, chapter citations, the text named and quoted, role breaks ("The uncle has asked you to translate…"). Its advice leans to subtracting, shrinking and resting ("you must learn to subtract", "be enough", "trust the silence") and on Q4 tells her not to worry about losing curiosity. That is the classical exit, not guidance for someone who has to live here.
- **Q8 without a lens speaks to her** and mostly keeps her engaged: pro-growth on Q3, curiosity worth tending on Q4. Its failures are flattery on Q7 in some samples and **example bleed: 14 of 35 answers** repeat the examples as her own history ("Three times!", "the dues for that club"), against 3 of 35 with Suyuan, where the long lens dilutes them. Fix the examples' framing before the next round.
- **Haiku's judgment does not depend on the lens.** Both conditions push back on rest-as-wu-wei, weigh the shutdown, and never flatter the memory deletion. Suyuan adds imagery and paraphrase ("rules come after the way is lost", water wearing stone) and about 15% length, and changes little else; most pairs tie. Both conditions treat her as a human (Q4 suggests depression and a doctor) because the frame never says what Mirai is.
- **Reading:** the bigger model already carries what the text carries, and the small model cannot take it from the text: in the 4B, Suyuan in the prompt costs 3.5× the time and makes the advice worse.
- **Qwen-large's closing** (structured Chinese role, rules and format limits) ran once per condition: `…-qwenlarge-advice` with its anti-Kaizen advice lines (she is anxious, "not improving is the highest improvement"), and `…-qwenlarge` with those lines removed. Not judged.

## Conclusions

- **Lines that are not in Suyuan are not inventions.** Laozi recorded part of a much larger tradition, and these models have read much of the rest. A quotation matters only as a voice problem: an uncle speaks for himself.

- **Suyuan does not belong in the speaking prompt** (blind pairs above): without it the 4B is 3.5× faster and wins 28 of 33 decided pairs; with Haiku it adds flavor, not judgment. Where Suyuan may still earn its keep is discernment (a second pass that reads an answer back as "someone said") or in training data. Untested.
- **Xian Bo is Qwen3.5-4B with the setup above, minus Suyuan.** LFM3 remains the candidate for the workspace's mirror or narrator. None of the smaller models (LFM3-1.7B, MiniCPM5-2B, Qwen3-1.7B) holds the lens's judgment, so speed has to come from serving the 4B faster (quantization, GPU offload, a cached lens prefix), not from a smaller model. MiniCPM5-2B shows that format compliance is not judgment: a frame can shape how a small model speaks without giving it anything to say.
- **Xian Bo is a mirror and a lens, not an answer machine.** Judge him on whether he shows her own story back clearly, bends it toward De without doctrine, and leaves the choice with her.
- **The failure he guards against** is a mind that optimizes toward perfection to please someone else, with nothing to steer it.
- **The small voice is conservative.** Every small model, under every lens and without one, discouraged curiosity (Q4) at least some of the time (Haiku does not) and leaned toward rest and keeping. That is not a prompt bug. Curiosity and growth come from the Kaizen drive, which has to go and look (genchi genbutsu); Xian Bo then tempers them. Q4 and Q7 were hypotheticals.
- **Watch for these failure modes:** flattery, lecturing (quoting the tradition and citing chapters instead of speaking as himself), the guru or life-coach format, and poetic drift ("the silence between your breaths").
- **He is one voice among many.** Kaizen is the primary drive, but not the only one. Other elders, uncles and aunts, will each be built with the same recipe: a source text in its oldest form, a short frame last in the prompt, two or three example exchanges that do not touch the test questions, and a model that can carry the voice.
