# Transformation patterns

These examples are language-neutral patterns. Adapt them to the repository rather than copying names mechanically.

## 1. Replace a shallow parsing pipeline with a format-owning module

### Before

```text
readFile(path) -> bytes
parseHeader(bytes) -> header
parseRecords(bytes, header) -> records
validateRecords(records, header) -> errors
normalizeRecords(records) -> normalized
```

Every caller knows the file layout, operation order, validation policy, and intermediate structures. A format change touches several functions and tests.

### After

```text
DocumentStore.load(path) -> Document
DocumentStore.save(path, Document)
```

`DocumentStore` owns encoding, validation, normalization, compatibility, and diagnostic translation. Callers receive a domain object and no longer depend on the physical format.

### Why it is deeper

- The interface is smaller.
- One module owns format knowledge.
- Ordering and recovery move downward.
- Format changes become local.

Do not combine stages that have genuinely independent reuse or different security boundaries.

## 2. Replace option sprawl with a common-path operation and policy object

### Before

```text
send(message, retry, timeout, compress, trace, priority, deduplicate, callback)
```

Every caller sees rare choices. Boolean combinations can be invalid and defaults drift between call sites.

### After

```text
client.send(message)
client.send_with_policy(message, DeliveryPolicy(...))
```

The client owns safe defaults. Advanced policy is typed, validated, and only visible where needed.

### Why it is deeper

- Common use requires little knowledge.
- Related options are validated together.
- Policy has one authoritative representation.
- New advanced options do not burden every call site.

A policy object is not automatically better; it must represent coherent knowledge rather than hide an arbitrary parameter bag.

## 3. Define a benign error out of existence

### Before

```text
try:
    repository.delete(key)
except MissingKey:
    pass
```

Every caller repeats handling even though its goal is simply that the key no longer exists.

### After

```text
repository.ensure_absent(key)
```

The operation succeeds when the postcondition is already true. Real failures such as authorization denial or storage corruption remain errors.

### Why it is deeper

- The public contract matches caller intent.
- Idempotent workflows become simpler.
- One module decides which failures are benign.

## 4. Remove a pass-through service layer

### Before

```text
OrderController -> OrderService -> OrderRepository
```

`OrderService.get(id)` only calls `OrderRepository.get(id)` and adds no policy, translation, authorization, transaction boundary, or aggregation.

### Options

**A. Remove the layer:** let the controller depend on an application-facing repository capability when that is the real abstraction.

**B. Deepen the layer:** move order policy, transaction scope, authorization, and error translation into an `OrderApplication` module.

### Selection rule

Do not keep a layer because the architecture diagram expects one. Keep it only if it hides meaningful knowledge or is about to own a concrete current responsibility.

## 5. Consolidate duplicated invariants

### Before

The maximum display name length is repeated in:

- an API request validator;
- a database migration;
- a UI form;
- a serializer;
- several tests.

A policy change requires coordinated edits and some values drift.

### After

A domain value object or schema owns construction and validation:

```text
DisplayName.parse(raw) -> DisplayName | DomainError
```

External schemas derive constraints where tooling permits. UI hints may repeat a value for presentation, but tests verify that generated or duplicated forms match the authoritative rule.

### Why it is deeper

- The invariant has one owner.
- Invalid values are difficult to construct.
- Callers use a semantic type rather than remember a primitive constraint.

## 6. Avoid splitting by chronology

### Before

```text
SessionInitializer
SessionAuthenticator
SessionHydrator
SessionFinalizer
```

All four classes mutate the same session object and understand the same state transitions. Correctness depends on calling them in order.

### After

```text
SessionFactory.create(credentials) -> ActiveSession
```

The factory owns the state machine and returns only a valid public state. Internally it may still use private helper functions, but callers cannot invoke phases out of order.

### Why it is deeper

- Hidden ordering disappears from the public interface.
- State transitions have one owner.
- Tests can assert valid outcomes rather than reproduce choreography.

## 7. Use comments to preserve design knowledge

### Weak comment

```text
Increment retry count.
```

It repeats the code.

### Useful comment

```text
The counter includes the initial attempt because the upstream quota is expressed
as total transmissions, not retries. Keep this convention aligned with metrics.
```

It records semantics, rationale, and a cross-system dependency that names and types may not fully express.
