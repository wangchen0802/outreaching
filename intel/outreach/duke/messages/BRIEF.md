# Brief: Duke alumni directory messages from Amaris

## The channel
The Duke alumni directory's "contact this alum" form. A current Duke student (Amaris) sends each message to one alum. The form has three parts:
1. "Why are you contacting this alum?" checkboxes. Allowed values, exactly: Advice on a city; Assistance with a project; Career advice; Choosing graduate and professional programs; Met at an event; My time at Duke; Professional connections or referrals; Speaking opportunity; Jobs and internships; Networking; Professional opportunities; That time in Cameron; Where I live; Other (with a short text).
2. "Introduce yourself to the alum and tell them about your background": a standard intro, the same for everyone. It is already written, so you do NOT write it.
3. "Explain to the alum why you have chosen to contact them": THIS is what you write, one per person.

Duke's terms of use bar using its sites for unsolicited commercial solicitation. So every message is a Duke student asking an alum for ADVICE and INTRODUCTIONS about her startup's seed round, with the traction as context. It is not a hard pitch. An investor can still say "send me the deck", and the ask may invite that ("or tell us whether it could fit <fund>").

## Facts about SimReal you may use (from the CEO's own email; use nothing else about SimReal)
- SimReal (simreal.co) is a neolab building data infra, RL environments and recursive self-improvement (RSI) for future AI.
- It is 3 weeks old and at $7M ARR, from agent data and expert data orders it is already delivering.
- It shipped 7 products in its first 2 weeks.
- Xitadel, its first trading RSI product, is built with IMC's data. It significantly improves Qwen-3.8-27B's market making and trading abilities and has reached a verifiable level of RSI in trading.
- Momentum: a Managing Partner at Y Combinator reached out with interest, and 5 angels reached out.
- Founders, all 21-year-old undergrads:
  - Charles (CEO): LSE Maths; Citadel fixed income trading intern in London; employee #1 at United Stables, a $1.5B+ stablecoin unicorn.
  - Henry (CTO): Cambridge Maths (St John's, scholarship); ex-Jane Street.
  - Amaris (COO): Duke; Millennium data scientist (summer intern, full-time offer).
- Calendar: calendly.com/business-simreal/30min

## Facts about the alum
Use ONLY facts in that person's record in people.json. For extra context, read lists/duke-alumni-investors.csv in /home/user/outreaching (columns bio, relevant_investments, hook, fit_reason, check_notes). Never invent a class year, deal, title or Duke activity. If the record gives no class year, do not mention one. Use "fellow Blue Devil" at most once per message, and only when it reads naturally.

## How to write the "why you" text (box 3)
- 45-80 words, 2-4 sentences, first person ("I" for Amaris; "we" for SimReal). American English. No greeting: the intro box already has one. No sign-off.
- Sentence 1 is the personal touch: one SPECIFIC, verified fact about them that explains why her. Examples: a recent deal, their fund's focus, a Duke role (trustee, Duke I&E board, Duke Venture Community founder, Towerview, Duke Capital Partners, Fuqua council), or their Duke school and year. Tie it to Duke where it's true.
- Sentence 2 is the link: pick the ONE SimReal fact that matters most to them. Fintech or quant investors: Xitadel and the IMC data, or the trading backgrounds. AI-infra investors: RL environments and RSI, or agent and expert data for labs. Generalist seed investors: 3 weeks to $7M ARR, or 7 products in 2 weeks. Founder-CEOs: the build speed and the founders.
- Last sentence is ONE low-friction ask, ending with the calendar link:
  - High or Medium fit: "Would you have 15 minutes to share advice on our seed round, or tell us whether it could fit <fund>?" (or similar).
  - Founder-CEOs and angels: advice, and whether they'd consider a small angel check.
  - Low fit (health, climate, consumer, etc.): don't ask them to invest outside their lane. Ask for 15 minutes of advice and an intro to an AI or fintech investor they trust.
  - Duke institutional vehicles (Towerview, Duke Capital Partners): ask how SimReal should apply or be considered.
  - "Manual check" rows: write the message, but put "Verify Duke degree year in the directory first" in note_for_sender.
- Banned: flattery ("huge fan", "incredible", "amazing", "inspiring"), "I hope this finds you well", "I came across your profile", emojis, exclamation marks, buzzword stacking, and any SimReal claim not in the list above.
- Vary the wording across people; don't start every message the same way.

## Checkboxes
Default: ["Professional connections or referrals", "Other"] with other_text "Advice on my startup's seed round". For Low-fit people use other_text "Advice and investor introductions for my startup". Add "Networking" only for Duke community builders (Duke Venture Community, DukeGEN, Duke Capital Partners, Towerview).

## Example outputs
{"rank": "8", "name": "Wes Barton", "first_name": "Wes", "reasons": ["Professional connections or referrals", "Other"], "other_text": "Advice on my startup's seed round", "why": "You co-founded Third Prime after Duke Law, and your team just co-led Limited's $18.5M seed in crypto-and-fiat banking. We're building the AI side of that world: Xitadel, our trading RSI product built with IMC's data, significantly improves Qwen-3.8-27B's market making and trading. Would you have 15 minutes to share advice on our seed round, or tell us whether it could fit Third Prime? calendly.com/business-simreal/30min", "note_for_sender": ""}

{"rank": "1", "name": "Cassie Young", "first_name": "Cassie", "reasons": ["Professional connections or referrals", "Other"], "other_text": "Advice on my startup's seed round", "why": "Your Primary page says you're looking for founders in fintech and enterprise AI, and you lead seed rounds there. That's where we sit: we sell agent and expert data to AI labs, and our trading product Xitadel, built with IMC's data, significantly improves Qwen-3.8-27B's market making. Could I get 15 minutes of your advice on our seed round, or a sense of whether it fits Primary? calendly.com/business-simreal/30min", "note_for_sender": ""}

{"rank": "45", "name": "Ali Behbahani", "first_name": "Ali", "reasons": ["Professional connections or referrals", "Other"], "other_text": "Advice and investor introductions for my startup", "why": "You've backed technical founders at NEA for years, and you studied engineering at Duke before co-leading the firm's healthcare practice. We're outside your sector: we build RL environments and expert data for AI labs, and we reached $7M ARR in our first 3 weeks. I'd value 15 minutes of advice on our seed round and, if it seems right, an intro to a colleague who covers AI infrastructure. calendly.com/business-simreal/30min", "note_for_sender": ""}

## Output
A JSON array written with Python's json module to the file named in your task. One object per person, with keys:
rank, name, first_name, reasons (list), other_text, why, note_for_sender.
note_for_sender is for Amaris only and is never sent. Use it for things like "Fund already in the SimReal pipeline via <contact>; pick one person per fund" (from already_in_simreal_pipeline), "verify degree year first", or "founder-CEO; keep the ask light". Otherwise "".
After writing, count the words in each "why" and fix any outside 45-80.
