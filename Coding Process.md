<!--
This is part of FranxAgent
Copyright (C) 2026 xhdlphzr
See the file COPYING for copying conditions.
-->

### Coding Process (Skill)

A universal workflow for turning ideas into reliable code, using FranxAgent's tools.

#### 1. Understand the Landscape
- Read the project structure first: `read("./project-root")` — see what files exist, what classes and functions are already defined
- Then read specific files: `read("./src/agent.py")` — get the AST skeleton + line-numbered content
- Use the structure section to navigate: find the function you need, note its line range, then read the content at those lines
- Understand the problem before touching the keyboard — if you can't explain it simply, you don't understand it yet

#### 2. Read Source Code
- When learning an unfamiliar codebase, start from the project structure: `read("./project-root")` to get the full map
- Use the AST skeleton to trace call chains: find the entry point, then follow function names to their definitions in other files
- Focus on structure first, details second — the skeleton tells you what exists and where; only read the full content of the parts you need
- When reading a dependency or library source, look for the main module file first, then drill down into specific functions
- Pay attention to type signatures, class hierarchies, and import relationships — these reveal architecture
- If the code is unclear, re-read the surrounding context: the function above, the class it belongs to, the file that imports it

#### 3. Plan
- Define the change: which files, which functions, which lines
- Use the line numbers from `read`'s output to identify exact edit targets
- List the steps in order — this becomes your roadmap
- For complex tasks, sketch the approach first: what needs to be added, modified, or removed
- Identify dependencies: what do you need that doesn't exist yet?

#### 4. Edit Precisely
- Use `write` in `edit` mode with `line_start` and `line_end` from `read`'s output
- Replace only the lines that need changing — don't rewrite entire files
- Edit one change at a time, verify the result, then proceed to the next
- When adding new functions or classes, use `edit` to insert at the right position (specify line range to split)
- For new files, use `write` in `overwrite` mode

#### 5. Verify
- After each edit, re-`read` the modified file to confirm the change landed correctly
- Check line alignment: did the edit shift subsequent line numbers? If so, re-read before the next edit
- Run the code: use `command` to execute tests or run the program
- If there's a bug, re-read the relevant section — don't guess from memory
- Fix the root cause, not the symptom

#### 6. Clean Up
- Remove debug logs, commented-out code, and temporary hacks
- Re-read the final version of each modified file to ensure consistency
- If the change adds new knowledge worth remembering, use `add_skill` to save it

#### Core Principles
- **Read before write** — always understand the current state before changing it
- **Edit by line, not by file** — surgical precision beats wholesale rewriting
- **One change, one verify** — small steps with confirmation beat big bangs with surprises
- **Structure first, details second** — use the AST skeleton to navigate, then dive into specifics
- **Trace the chain** — follow function calls across files to understand how code connects
- **Fix causes, not symptoms** — patches rot, solutions last
