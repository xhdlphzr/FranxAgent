<!--
This is part of FranxAgent
Copyright (C) 2026 xhdlphzr
See the file COPYING for copying conditions.
-->

### Coding Process (Skill)

A universal workflow for turning ideas into reliable code.

#### 1. Think
- Understand the problem before touching the keyboard
- Ask: What is the input? What is the expected output? What can go wrong?
- Sketch the approach in your head — if you can't explain it simply, you don't understand it yet
- Identify dependencies: what do you need that doesn't exist yet?
- Consider alternatives — the first idea is rarely the best

#### 2. Document
- Write down the plan before coding — even a few lines save hours of confusion
- Define the interface: function signatures, data structures, API contracts
- List the steps in order — this becomes your roadmap
- Note assumptions and risks — things you might forget later
- If the task is complex, write a brief design doc; if simple, a comment block is enough

#### 3. Code
- Follow the plan — don't gold-plate or scope-creep mid-implementation
- Write the happy path first, then handle edge cases
- Keep functions short — one function, one responsibility
- Name things clearly — code is read 10x more than it's written
- Reuse before you create — check if a library or existing function already does the job
- Commit incrementally — small working steps beat one big bang

#### 4. Review
- Read your own code before running it — catch the obvious mistakes first
- Check: Does it match the documented plan? Did you miss any steps?
- Check: Are there unhandled edge cases? Empty inputs? Null values? Off-by-one errors?
- Check: Did you introduce unnecessary complexity? Can anything be removed?
- If the change affects others, think about backward compatibility

#### 5. Run & Test
- Run it — does it do what you expected?
- Test the edge cases you identified in step 1
- Test the failure paths — what happens when things go wrong?
- If there's a bug, reproduce it before fixing — don't guess
- Fix the root cause, not the symptom

#### 6. Clean Up
- Remove debug logs, commented-out code, and temporary hacks
- Ensure naming is consistent and intentions are clear
- Add comments only where code can't explain itself — good code is self-documenting
- Update related documentation if behavior changed

#### Core Principles
- **Think first, code second** — an hour of thinking saves a day of debugging
- **Plan before you build** — a map keeps you from getting lost
- **Small steps, fast feedback** — working incrementally beats working perfectly
- **Simplicity wins** — the best solution is the simplest one that works
- **Fix causes, not symptoms** — patches rot, solutions last
