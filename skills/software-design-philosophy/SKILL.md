---
name: software-design-philosophy
description: "Design, review, or refactor software to reduce complexity using deep modules, information hiding, change locality, low cognitive load, error elimination, and design-twice comparisons. Use for architecture, API, module-boundary, maintainability, or refactoring work, including requests mentioning 软件设计、复杂度、深模块 or 信息隐藏. Do not use for formatting-only or dependency-version tasks."
---

# Software Design Philosophy

Apply the design principles popularized by John Ousterhout's *A Philosophy of Software Design* as a practical engineering workflow. Optimize for the long-term cost of understanding and changing the system, not only for finishing the current patch.

Use the user's language for explanations unless repository conventions require another language. Keep code, identifiers, and public API terminology consistent with the repository.

## Core objective

Reduce complexity as experienced by future maintainers. Diagnose complexity through three observable symptoms:

1. **Change amplification**: a small requirement forces edits in many places.
2. **Cognitive load**: a developer must hold too much context to make a safe change.
3. **Unknown unknowns**: important dependencies or consequences are difficult to discover before editing.

Do not equate quality with short files, tiny methods, more classes, or more abstractions. A larger implementation can be better when it presents a substantially simpler interface and hides more knowledge.

## Operating rules

- Inspect the relevant code, tests, docs, call sites, and repository instructions before prescribing a design.
- Separate evidence from inference. Cite concrete files, symbols, call paths, or tests when reviewing an existing codebase.
- Preserve externally observable behavior unless the task explicitly requests a behavior or API change.
- Prefer the smallest coherent change that improves the abstraction. Do not scatter partial fixes across layers.
- Do not introduce an abstraction merely to remove a few duplicated lines. Abstract shared knowledge, policy, or invariants.
- Do not add configuration, exceptions, callbacks, or public methods unless their caller-side cost is justified.
- When implementation is requested, complete the change and run the most relevant available validation. When only review or planning is requested, do not edit files.
- Treat urgent tactical patches explicitly: contain the shortcut, record the debt, and avoid making the shortcut part of the public contract.

## Workflow

### 1. Frame the design problem

Establish:

- the user-visible outcome;
- current behavior and compatibility constraints;
- performance, security, reliability, and delivery constraints;
- the public or internal interfaces affected;
- the likely future changes the design should make easy.

Do not assume a rewrite is allowed. If the request is ambiguous, infer the narrowest safe scope from repository evidence and state the assumption.

### 2. Build a complexity map

Trace the requested change through the system. Identify:

- which modules know each relevant rule or representation;
- which callers must understand order, state, configuration, ownership, or failure details;
- where a single decision is duplicated;
- where edits would propagate;
- where behavior is implicit, surprising, or difficult to test.

Classify findings using the symptom names above. Open `references/principles.md` when a deeper diagnostic catalogue is useful.

### 3. Locate the design causes

Look specifically for:

- shallow modules whose interface is nearly as complex as their implementation;
- information leakage across module boundaries;
- temporal decomposition, where phases are separated even though each phase must know the same representation or state machine;
- pass-through methods or layers that add little abstraction;
- configuration and exception sprawl;
- special-case logic mixed into general-purpose code;
- vague names, inconsistent conventions, and interfaces that are hard to describe;
- comments that repeat syntax while omitting invariants, rationale, units, ownership, or constraints.

Rank causes by maintenance impact, not by visual untidiness.

### 4. Design it twice

For any non-trivial module, API, data model, or refactor, produce at least two meaningfully different alternatives before selecting one. Alternatives must differ in responsibility placement, interface shape, data ownership, or error semantics; renaming the same design does not count.

For each alternative, sketch:

- the interface seen by callers;
- the knowledge hidden inside the module;
- dependencies introduced or removed;
- common-path usage;
- failure semantics;
- migration and testing cost.

Compare the alternatives using `references/review-rubric.md`. Prefer the option that lowers total system complexity, even if its implementation is locally more sophisticated.

### 5. Apply the decision rules

Use these rules in order:

1. **Create deep modules.** Seek a small, stable interface that provides substantial capability.
2. **Hide information.** Keep each important format, policy, invariant, protocol, or design decision authoritative in one place.
3. **Pull complexity downward.** Let a module absorb difficult defaults, sequencing, recovery, caching, or bookkeeping when that saves many callers from repeating it.
4. **Keep interfaces somewhat general.** Support the current family of needs without exposing current workflow accidents or building speculative features.
5. **Eliminate error cases where possible.** Redefine operations so benign states are normal outcomes, recover internally when safe, and aggregate handling at deliberate boundaries.
6. **Optimize the common path.** Common operations should require little knowledge and few parameters; rare capabilities should not burden every caller.
7. **Make the design obvious.** Use precise names, consistent patterns, explicit invariants, and comments at the appropriate abstraction level.
8. **Prefer change locality.** A future policy change should have one obvious home and minimal ripple effects.

### 6. Implement or produce the plan

When editing code:

- move responsibilities to the module that owns the underlying knowledge;
- simplify the caller-facing interface before polishing internals;
- remove obsolete pass-through APIs and duplicated policy when compatibility permits;
- provide migration shims only when they reduce rollout risk, and mark their removal path;
- write interface comments before or alongside implementation for non-obvious contracts;
- update tests at the abstraction boundary, including representative failure behavior;
- avoid unrelated cleanup that makes review harder.

When producing only a plan, name the files or components likely to change, define sequencing, state compatibility risks, and give a test strategy.

### 7. Validate the result

Verify:

- the requested behavior works;
- the common path is simpler for callers;
- relevant knowledge has one authoritative location;
- no new hidden ordering or ownership dependency was introduced;
- exceptions and configuration are no broader than necessary;
- tests exercise the public abstraction rather than incidental implementation details;
- the design can be explained briefly without a list of caveats.

Use `assets/design-review-template.md` for substantial reviews or proposals. Use `references/examples.md` when a concrete transformation pattern is helpful.

## Red flags that require explicit justification

- A new public method merely forwards arguments.
- One concept requires coordinated edits in several modules.
- A caller must know an internal storage format or state transition.
- A method has many flags or optional parameters for unrelated modes.
- A benign, expected state is represented as an exception.
- A class is split only because of method length or chronology.
- An abstraction has one trivial implementation and no meaningful hidden policy.
- The same invariant appears in validation, serialization, UI, and tests independently.
- A design is selected without comparing an alternative.
- An interface comment cannot be written concisely because the contract has too many caveats.

## Output contract

For a design review or refactoring proposal, provide:

1. **Context and constraints**
2. **Complexity diagnosis**, tied to concrete evidence
3. **Two alternatives**, including caller-facing interface sketches
4. **Decision and rationale**
5. **Change plan or implemented changes**
6. **Validation performed**
7. **Residual risks or deliberate trade-offs**

Keep the final recommendation decisive. Do not hide behind a checklist or present all alternatives as equally good when the evidence favors one.

For a small implementation where a full review would be excessive, keep the same reasoning internally and summarize only the most important design choice and validation.

## Supporting resources

- `references/principles.md`: detailed principle catalogue and diagnostic questions.
- `references/review-rubric.md`: comparison and review scoring rubric.
- `references/examples.md`: language-neutral before/after patterns.
- `assets/design-review-template.md`: reusable review document template.
