# Brief: deeper search for Duke-alumni seed and angel investors

## Who it is for
SimReal (simreal.co) is a seed-stage AI startup. It builds RL environments, verifiers and expert data for LLM post-training; its flagship is Xitadel, a trading environment that lifted an open model's trading performance 12% on unseen market data. The founders are quants from Cambridge, LSE and Duke (COO Amaris is a current Duke undergraduate). They are raising a seed round and will cold-email Duke alumni themselves.

## Who qualifies (all must hold)
1. A Duke University degree (Trinity/Pratt undergrad, Fuqua MBA incl. weekend/global executive MBA, Duke Law, Duke Med, Duke Graduate School) COMPLETED IN 2018 OR EARLIER. Duke Kunshan-only, exec-ed certificates and "Fuqua network" membership on Signal do NOT count. The year may be stated ("T'96", "'05", "MBA 2004") or certain from career (e.g. "partner since 2011").
2. Writes ANGEL / PRE-SEED / SEED checks in 2025-2026, as one of:
   - an active angel investing their own money (operator-angels, syndicate leads, angel-group members with named deals),
   - a solo GP or micro-VC / pre-seed / seed fund founder or GP,
   - a decision-making partner at a seed fund.
   Associates, analysts, scouts with no own capital, growth-only, buyout and public-market roles do not count. A scout who also angel-invests their own money counts only with named deals.
3. Not already known: skip everyone in `known_people.json` (keys: included, excluded, not_duke), which sits in the same scratchpad folder. Do not spend searches on them.

## Rules
- Today is 2026-10-05 and your training knowledge is stale, so verify with WebSearch. Load WebSearch and WebFetch via ToolSearch with query "select:WebSearch,WebFetch". WebFetch/curl to most sites is blocked by a proxy, so rely on search-result snippets. Do not retry blocked domains. If WebSearch says the budget is used up, stop and write what you have.
- Public professional information only. Never guess a name, title, school, year or email. Never add a person from memory alone: memory is only a reason to run a search.
- Email: record one ONLY if the person or their employer published it (own site/blog/newsletter, fund site, official release, an interview where they say "email me at"). Never construct one from a pattern, never search for a guessed full address, never use or cite data-broker / email-finder sites (RocketReach, ZoomInfo, Apollo, Hunter, ContactOut, SignalHire, Lusha, Clearbit, "email format" pages, etc.). Otherwise "not found".
- Do not log in to or interact with LinkedIn, X or any platform; a profile URL seen in a search result may be cited. Do not contact anyone. Do not edit the git repository.
- Every fact needs a source URL suffixed " (search snippet)" or " (read)".

## Output
Write a JSON object with Python's json module to the file named in your task:
{"people": [ ... ], "checked_not_qualifying": ["Name (one-line reason)", ...], "searches_used": N, "coverage_notes": "..."}

Each person:
{"name", "include": true/false, "exclude_reason", "firm" (current vehicle, or "Angel investor"), "title_2026", "location",
 "still_active_2026": "yes"/"no"/"unclear", "decision_maker": "yes"/"unclear"/"no", "role_sources": [..],
 "duke_degree", "duke_grad_year": int or null, "grad_year_basis", "duke_sources": [..],
 "stage_focus", "sectors", "bio" (2-3 sentences, max 60 words, sourced facts only),
 "relevant_investments" (AI / data / infra / fintech / quant / dev-tools deals with year; "none found" otherwise), "investment_sources": [..],
 "email", "email_source", "other_contact" (official fund pitch inbox or form, with source), "linkedin_url", "x_url", "personal_site",
 "fit": "High"/"Medium"/"Low", "fit_reason",
 "hook" (ONE sentence, max 35 words, second person, "You <verified thing>; we <SimReal link>."; "" if no verified fact), "hook_sources": [..],
 "confidence": "High"/"Medium"/"Low"}

Fit: High = angel/seed checks into AI infrastructure, data, ML tooling, developer tools, fintech, trading/quant or capital-markets tech, with recent activity. Medium = generalist early-stage tech / B2B software / crypto, or strong focus but small or uncertain activity. Low = sector mismatch (healthcare, climate, consumer brands, real estate) or weak activity.

Include people who fail a criterion only if you checked them carefully (include=false with exclude_reason); list quick rule-outs in checked_not_qualifying.
