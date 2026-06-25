# Software design review

## 1. Context and constraints

- User-visible outcome:
- Current behavior:
- Compatibility constraints:
- Performance, security, reliability, and delivery constraints:
- Likely future changes:
- Scope assumptions:

## 2. Complexity diagnosis

### Change amplification

- Evidence:
- Expected blast radius:

### Cognitive load

- Evidence:
- Knowledge required by callers or maintainers:

### Unknown unknowns

- Evidence:
- Hidden dependencies or surprising consequences:

### Root design causes

- Shallow modules:
- Information leakage:
- Temporal decomposition:
- Pass-through layers:
- Error/configuration sprawl:
- Naming/documentation gaps:

## 3. Alternative A

### Caller-facing interface

```text

```

### Knowledge hidden

- 

### Dependencies and ownership

- 

### Failure semantics

- 

### Migration and tests

- 

### Rubric highlights

- Strengths:
- Weaknesses:

## 4. Alternative B

### Caller-facing interface

```text

```

### Knowledge hidden

- 

### Dependencies and ownership

- 

### Failure semantics

- 

### Migration and tests

- 

### Rubric highlights

- Strengths:
- Weaknesses:

## 5. Decision

- Selected option:
- Primary reason:
- Future-change scenarios tested:
- Rejected trade-off:

## 6. Change plan or implementation summary

1. 
2. 
3. 

## 7. Validation

- Automated tests:
- Static checks:
- Manual checks:
- Compatibility/rollback check:

## 8. Residual risks

- Risk:
- Mitigation or observation plan:
