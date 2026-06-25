# Software design review rubric

Use this rubric to compare alternatives or review an existing design. Scores support judgment; they do not replace it.

## Scoring

Score each dimension from 0 to 3:

- **0 — harmful**: the design creates substantial complexity or hides a serious risk.
- **1 — weak**: the design works but exposes avoidable complexity.
- **2 — sound**: the design manages complexity adequately with minor trade-offs.
- **3 — strong**: the design clearly reduces system-wide complexity and has evidence to support it.

A security, correctness, durability, or compatibility blocker overrides the total score.

## Dimensions

### 1. Interface depth

- 0: callers understand most implementation details or follow a fragile sequence.
- 1: some capability is hidden, but the interface remains broad or procedural.
- 2: common operations are concise and most implementation details are hidden.
- 3: a small stable interface provides substantial capability and sensible defaults.

### 2. Information hiding

- 0: core knowledge is duplicated across multiple modules.
- 1: ownership exists but callers still inspect internal representation or repeat policy.
- 2: most knowledge has an authoritative owner with limited leakage.
- 3: representation, policy, invariants, and transitions are encapsulated behind semantic operations.

### 3. Change locality

- 0: expected changes require coordinated edits across unrelated areas.
- 1: changes are partly localized but still ripple through several callers.
- 2: most changes have one primary home and a small predictable blast radius.
- 3: likely future changes are isolated behind stable boundaries and covered by boundary tests.

### 4. Cognitive load and discoverability

- 0: safe use depends on hidden order, state, flags, or undocumented conventions.
- 1: the design is learnable only by tracing several layers or examples.
- 2: names, types, and docs make normal use understandable.
- 3: the obvious use is correct, dependencies are visible, and misuse is difficult.

### 5. Dependency quality

- 0: cycles, broad coupling, or shared mutable state dominate.
- 1: dependency direction is mostly sensible but contains pass-through layers or unnecessary reach-through.
- 2: dependencies align with ownership and abstraction boundaries.
- 3: high-level policy depends on stable capabilities, and implementation details cannot leak upward accidentally.

### 6. Error and configuration surface

- 0: callers handle many implementation-specific errors or mandatory options.
- 1: some defaults and translation exist, but normal states still create noise.
- 2: benign states are normalized, failures are meaningful, and common use needs little configuration.
- 3: errors are eliminated or contained where safe, advanced policy is opt-in, and observability remains strong.

### 7. Appropriate generality

- 0: the design is either one-use hard-coded or highly speculative.
- 1: the abstraction is tied to workflow details or contains unused extension points.
- 2: it serves the current family of use cases without unnecessary features.
- 3: it captures a stable domain concept and simplifies several real current uses.

### 8. Obviousness, naming, and documentation

- 0: vague terms, inconsistent conventions, or missing contract information create ambiguity.
- 1: implementation can be understood, but key rationale or invariants are implicit.
- 2: names and interface docs communicate the abstraction and constraints.
- 3: the design is easy to explain, terminology is consistent, and comments preserve non-obvious knowledge.

### 9. Migration and verification

- 0: rollout risk is unaddressed and behavior cannot be verified confidently.
- 1: migration or testing is described only at a high level.
- 2: compatibility, sequencing, rollback, and boundary tests are concrete.
- 3: the design supports incremental migration with measurable validation and a removal path for temporary shims.

## Comparison method

1. Reject any option with an unresolved blocker.
2. Record evidence for every score; avoid scoring from taste alone.
3. Compare the three most important dimensions for the specific task, not only totals.
4. Test each option against two likely future changes.
5. Prefer the lower-complexity option unless another constraint has greater documented importance.
6. State the trade-off retained by the selected option.

## Review summary format

- **Decision**: selected option or required change.
- **Primary reason**: the most important complexity reduction.
- **Evidence**: concrete callers, modules, or change scenarios.
- **Rejected alternative**: why it loses despite any local advantage.
- **Risk**: remaining concern and how it will be validated.
