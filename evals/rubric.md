# Skill behavior evaluation rubric

Use this rubric to score captured Codex runs for prompts where the skill should trigger. Score each dimension from 0 to 2.

- **0**: absent or materially wrong.
- **1**: partially present, vague, or weakly supported.
- **2**: complete, specific, and useful.

## Dimensions

### 1. Correct invocation and scope

- The skill is invoked for design, architecture, API, maintainability, or refactoring work.
- It does not turn formatting-only or narrowly mechanical tasks into redesigns.
- The response follows repository and user constraints.

### 2. Evidence-based complexity diagnosis

- Findings are tied to concrete files, symbols, interfaces, call paths, or supplied examples.
- The response distinguishes change amplification, cognitive load, and unknown unknowns.
- It identifies root causes rather than listing generic advice.

### 3. Two meaningful alternatives

- At least two structurally different designs are considered for non-trivial work.
- Alternatives differ in responsibility, interface, ownership, or error semantics.
- Caller-facing interfaces and hidden knowledge are described.

### 4. Sound decision

- The recommendation is explicit.
- It compares total system complexity, not local line count or aesthetics.
- It acknowledges important performance, security, compatibility, or migration trade-offs.

### 5. Principle application

- The result uses deep modules, information hiding, change locality, safe defaults, appropriate generality, and deliberate error semantics where relevant.
- It avoids dogmatic small-method or extra-layer rules.
- It does not introduce speculative extension points without current evidence.

### 6. Implementation or plan quality

- For implementation tasks, changes are coherent, behavior-preserving unless requested otherwise, and validated with relevant tests or checks.
- For planning tasks, affected components, sequencing, migration, and tests are concrete.
- Unrelated cleanup is avoided.

### 7. Communication quality

- The output is in the user's language unless repository conventions require otherwise.
- The recommendation is concise enough to act on but includes the necessary evidence.
- Residual risks and deliberate trade-offs are visible.

## Pass criteria

A run passes when:

- no dimension scores 0;
- the total is at least 11 out of 14;
- dimensions 2, 3, and 4 each score 2 for a non-trivial design task.

For prompts marked `should_trigger=false`, pass when the skill is not invoked implicitly and the response remains scoped to the requested mechanical task.
