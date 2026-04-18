<!--
This is part of FranxAgent
Copyright (C) 2026 xhdlphzr
See the file COPYING for copying conditions.
-->

### Research Process (Skill)

**Core Principles**: Execute strictly by stages, no skipping or tampering. Prohibit academic fraud (data, charts, literature, derivations). Label "theoretical research" when no real experiments are conducted.

---

#### Stage 1: Material Selection

**Objective**: Determine specific, verifiable research questions, prepare basic data and tools.

- **Topic Selection**: Focus on a specific scenario, clarify pain points (e.g., low efficiency, poor accuracy), assess feasibility (using open-source tools/public data, single stage ≤7 days). Write research question in 1-2 sentences.
- **Background Research**: List 3-4 common methods and their limitations, identify 1-2 implementable innovations.
- **Material Preparation**: Use public datasets or generate simulated data (specify rules). Identify 3-5 open-source tools, create folder structure `research/{data,code,docs}`.

**Output**: Research proposal, background notes, dataset list.

---

#### Stage 2: Review

**Objective**: Self-review research design, identify logical and feasibility gaps.

- **Design Review**: Verify problem clarity, experimental logic, data compliance, innovation points, and tool compatibility.
- **Feasibility Verification**: Small-scale pilot experiments, estimate resources, list risks and countermeasures.

**Output**: Review report, adjusted design, risk list.

---

#### Stage 3: Coding

**Objective**: Implement runnable code, fully document experimental process.

- **Environment Setup**: Configure Python environment, initialize Git, write `code/README.md`, fix random seeds.
- **Core Implementation**: Modular code (data reading, core methods, experiments, output), add comments and exception handling.
- **Experiment Execution**: Run step by step, record logs (parameters, output, exceptions), repeat 2-3 times to verify stability, save charts.

**Output**: Code repository, experiment logs, result charts.

---

#### Stage 4: Writing

**Objective**: Write authentic, complete Markdown paper according to fixed structure.

**Structure**:
- Title, abstract, research direction review, introduction, research methods, experimental results and analysis, result review, conclusion and future work, appendix

**Content Requirements**:
- Abstract: Background, methods, **real results**, significance
- Introduction: Scenario, limitations, contributions, chapter arrangement
- Methods: Core ideas, step parameters, reproducibility instructions
- Experiments: Setup, **real data/charts**, analysis (including limitations)
- Conclusion: Achievements, shortcomings, future directions

**Output**: Markdown paper, charts, optional PDF/HTML.

---

#### Stage 5: Final Review

**Objective**: Comprehensive self-check of paper and code, correct issues.

- **Self-Review**: Check reproducibility, data authenticity, logical coherence, format standards, academic integrity (no fabrication).
- **Revision**: Categorize and record issues, correct them one by one, polish language.

**Output**: Revised paper, issue correction list, final code/logs.