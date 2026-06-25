# Principle catalogue

This reference translates the ideas associated with *A Philosophy of Software Design* into questions and actions for software work. It is an original operational summary, not a substitute for the book.

## 1. Complexity is the primary design cost

Complexity is anything that makes a system harder to understand or modify safely. It is experienced through:

- **Change amplification**: one conceptual change requires edits in several places.
- **Cognitive load**: the developer must understand many concepts at once.
- **Unknown unknowns**: the system does not reveal what else may break.

### Diagnostic questions

- How many files, modules, schemas, or tests would a small policy change touch?
- What facts must a new maintainer know before making a safe edit?
- Are dependencies visible from interfaces and naming, or discovered only after failures?
- Is complexity concentrated behind a boundary, or repeated by every caller?

### Actions

- Move repeated knowledge to one owner.
- Make dependencies explicit at the right abstraction level.
- Reduce the number of concepts required for the common path.
- Prefer designs whose consequences are discoverable from the interface.

## 2. Practice strategic programming

Tactical programming optimizes only for the current task. Strategic programming also invests in the structure that future work will reuse.

This does not justify gold-plating. The investment should be directly connected to reducing recurring complexity around the current change.

### Diagnostic questions

- Is the patch adding another special case to an already fragile path?
- Will the next similar feature copy this logic again?
- Is a small boundary improvement available now at modest cost?
- Is delivery pressure being used to turn a temporary shortcut into a permanent API?

### Actions

- Spend a small, deliberate portion of the task on improving the relevant abstraction.
- Contain unavoidable shortcuts and document their removal condition.
- Avoid broad rewrites that are not necessary to create a better boundary.

## 3. Prefer deep modules

A deep module offers substantial capability through a small, understandable interface. Depth is the ratio between functionality hidden and complexity exposed.

A module is shallow when callers must understand nearly as much as the implementation author, even if the module has few lines.

### Diagnostic questions

- Does the interface save callers from knowing internal representation, ordering, or recovery details?
- Would removing the wrapper make calling code almost the same?
- Does the module provide a coherent capability or only rename another API?
- Can common use be shown in a few obvious operations?

### Actions

- Combine responsibilities that share the same hidden knowledge.
- Remove pass-through methods that do not enforce policy or simplify usage.
- Accept a more substantial implementation when it creates a simpler contract.
- Avoid splitting code solely to meet arbitrary file or method size targets.

## 4. Hide information and design decisions

Each important piece of knowledge should have one authoritative home. Examples include file formats, protocol rules, database mappings, retry policy, cache invalidation, units, and state-machine transitions.

Information leakage occurs when several modules must understand the same decision.

### Diagnostic questions

- Which module owns this rule?
- Is the rule duplicated in validation, serialization, UI, tests, or callers?
- Would changing an internal representation require caller edits?
- Do several phases inspect the same raw structure independently?

### Actions

- Put behavior next to the knowledge it depends on.
- Expose semantic operations rather than raw representation.
- Centralize invariants and derive secondary forms from the source of truth.
- Keep tests focused on contracts; avoid duplicating implementation algorithms as fixtures.

## 5. Avoid temporal decomposition

Temporal decomposition splits code according to execution order even when phases share one representation or invariant set. Examples include separate read, parse, validate, normalize, and emit modules that all know the same format.

Chronology is not always a useful abstraction boundary.

### Diagnostic questions

- Do several sequential stages all understand the same schema or state machine?
- Is data passed through a chain of structures that differ only slightly?
- Would a format change require coordinated edits in every phase?
- Is there a coherent capability that could own the end-to-end transformation?

### Actions

- Group phases that share hidden knowledge behind one semantic interface.
- Expose the result callers need, not every intermediate step.
- Keep independent phases separate only when they genuinely have different knowledge, lifecycles, or reuse.

## 6. Make modules somewhat general-purpose

A useful module handles the current family of problems through a stable abstraction. It is neither tied to one workflow accident nor expanded for speculative futures.

### Diagnostic questions

- Does the interface describe the problem domain or one current screen, endpoint, or job?
- Are special-case flags accumulating because the abstraction is too narrow?
- Would a modestly more general operation simplify multiple current callers?
- Is proposed generality backed by real nearby use cases?

### Actions

- Generalize the interface before generalizing every implementation detail.
- Choose domain concepts that remain stable across current use cases.
- Reject speculative extension points that add permanent caller complexity.
- Keep specialized policy outside a general mechanism when the knowledge differs.

## 7. Pull complexity downward

The module author should absorb complexity when doing so prevents many callers from handling it repeatedly. Examples include defaults, bookkeeping, batching, recovery, state management, and resource cleanup.

### Diagnostic questions

- Are all callers performing the same setup, validation, retry, or cleanup?
- Can the module infer a safe default?
- Is the caller forced to manage an internal state machine?
- Would one robust implementation replace many fragile call-site conventions?

### Actions

- Automate common sequencing and cleanup.
- Provide safe defaults and make advanced policy opt-in.
- Keep resource ownership explicit and preferably local.
- Do not push exceptions or configuration upward merely to keep the implementation simple.

## 8. Define errors out of existence

Some failures disappear when an operation is defined around the caller's goal rather than a narrow mechanism. For example, an operation that ensures absence need not fail when the item is already absent.

Not every error can or should be hidden. Security violations, data corruption, and broken invariants must remain visible.

### Diagnostic questions

- Is this condition genuinely exceptional for the caller?
- Can the operation be idempotent?
- Can the module recover safely without losing important information?
- Can several low-level failures be translated into one meaningful boundary error?
- Is the caller capable of acting on the detailed error being exposed?

### Actions

- Normalize benign states into successful outcomes.
- Recover internally when behavior is deterministic and safe.
- Translate implementation-specific failures at module boundaries.
- Aggregate handling at a layer with enough context to decide.
- Preserve causality for diagnostics even when the public error surface is smaller.

## 9. Design it twice

The first workable design is often shaped by existing code or the first idea that occurred. Comparing alternatives exposes hidden assumptions.

### Diagnostic questions

- What changes if responsibility moves one layer down or up?
- What would the interface look like if callers never saw the internal representation?
- Could the operation be modeled as a capability, data transformation, or policy object instead?
- Which option has the smallest common-path interface?
- Which option localizes the most likely future changes?

### Actions

- Sketch two interfaces before implementation for non-trivial work.
- Make alternatives structurally different.
- Compare using concrete future changes, not aesthetic preference.
- Record why the selected design wins and what trade-off remains.

## 10. Make important things obvious

Good naming, consistency, and documentation reduce the need to inspect implementation details.

### Names

- Use the same word for the same concept across layers.
- Avoid vague names such as `data`, `manager`, `helper`, `process`, or `handle` when a precise domain term exists.
- Include units or ownership in names when ambiguity would be dangerous.
- Distinguish concepts clearly; do not use near-synonyms for different semantics.

### Comments

Comments should explain information that code alone does not express well:

- the abstraction and contract;
- rationale and rejected alternatives;
- invariants and ownership;
- units, bounds, ordering, and concurrency assumptions;
- why apparently unnecessary code must remain.

Do not narrate syntax. If the interface comment requires many caveats, reconsider the interface.

## 11. Use consistency as a complexity tool

Consistency lets developers transfer knowledge from one part of the system to another. It is valuable when the underlying concepts are genuinely the same.

### Diagnostic questions

- Do similar operations use similar names, argument order, error behavior, and ownership rules?
- Are differences intentional and visible?
- Is a local convention being invented without a concrete benefit?

### Actions

- Follow established repository patterns unless they create the problem being fixed.
- When introducing a better pattern, migrate a coherent boundary rather than mixing conventions unpredictably.
- Document intentional deviations.

## 12. Evaluate the whole system, not local elegance

A locally elegant abstraction can increase total complexity if it adds indirection, configuration, or another place to search.

### Diagnostic questions

- Who pays the complexity cost: one module author or every caller?
- Does this layer remove knowledge or only relocate code?
- Does the design reduce the number of concepts in the system?
- Will debugging require jumping through more layers?

### Actions

- Optimize for total maintenance cost.
- Prefer one obvious place to understand a behavior.
- Remove abstractions that no longer hide meaningful decisions.
- Keep performance, reliability, and security constraints explicit; lower complexity must not erase essential guarantees.
