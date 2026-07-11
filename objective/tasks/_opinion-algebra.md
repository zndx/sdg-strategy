# Opinion Algebra (shared)

Normative surface for tasks that produce or consume **subjective opinions**
(boundary-relative or first-order). Task cards include this module by reference;
do not maintain a divergent copy of the bijection, bins, or operator list.

## Opinion

An **opinion** on a binary proposition is ω = (b, d, u, a) with b + d + u = 1:

| symbol | role |
|--------|------|
| **b** | belief mass for the proposition |
| **d** | disbelief mass against it |
| **u** | uncertainty mass (uncommitted epistemic residual) |
| **a** | base rate (prior used when projecting expectation from residual u) |

**Projected probability** (expectation): P ≈ b + a·u.  
Because a weights the unresolved mass, **a is load-bearing precisely when u is high** — the usual regime in metrology and blind settings.

**Multinomial opinions** assign belief masses over a frame of categories (or taxonomy subtrees) plus a shared u; each category may carry its own base rate a(·) over the frame.

## Qualitative bins (default)

Qualitative answers are licensed when consistent with the trace. Approximate bands when numbers are used:

| qualitative | approximate numeric band |
|-------------|--------------------------|
| near-vacuous / very high u | u ≳ 0.6 |
| high u / thin evidence | u ∈ [0.35, 0.6) |
| moderate commitment | u ∈ [0.15, 0.35), dominant b or d clear |
| low u / strong evidence | u < 0.15 |

"Thin evidence" in this table means **high uncertainty mass**, not a product-label synonym for "bad."

## Evidence ↔ opinion (beta bijection)

When a specimen supplies evidence counts, the ground-truth map is the **beta–opinion bijection** with default non-informative weight **W = 2**:

```
b = r / (r + s + W)
d = s / (r + s + W)
u = W / (r + s + W)
```

- **r** — positive evidence mass (admitted confirming signals, under the specimen's counting rule)
- **s** — negative evidence mass (admitted disconfirming signals)

Ground truth for a participant's opinion is **computable from the simulated trace**: count what crossed its membrane, apply the bijection, apply the stated base rate. No free-text mental-state grading is required.

## Base rates are first-class

Base rate **a** is part of the **boundary / frame specification**, not an authorial free parameter:

- Specimens SHOULD pin a (or a(·) over a multinomial frame) in the boundary topology or frame prior.
- Prefer values **computable from the setup**: uniform over n live candidates ⇒ a = 1/n; empirical frequency in a declared vocabulary subtree; symmetric a = 0.5 only when the frame is binary and no prior is supplied.
- When a is omitted, the answer may leave projected probability underdetermined and must say so; it must not silently invent a.

## Labels are lossy projections (**label collapse**)

Scalar product labels (e.g. structural verdicts `thin` / `rich`, traffic-light scores, "consistent") are **not opinions**. They are lossy projections of an underlying ω relative to a membrane and a counting rule.

The same label can name **distinct opinion states**. Classic case — the label **thin**:

| recovered ω shape | what "thin" was collapsing |
|-------------------|----------------------------|
| high **u**, low b and d | ignorance / insufficient evidence (small r+s) |
| high **d**, moderate u | confident disbelief with residual (large s, modest r) |

**Label collapse** is a named phenomenon: recovering *which* opinion state obtains from the trace (counts, notes, ordering) is a first-class reasoning skill. A scalar verdict is where measurement integrity often leaks — the projection discards whether the membrane was uncertain or was certain of a negative.

Do not equate a label with a unique (b, d, u). Always re-derive ω from admitted evidence when counts or notes permit; treat the label as a costume over that recovery.

## Proposition scope vs discount

Two distinct moves, often confused:

| move | question | correct handling |
|------|----------|------------------|
| **Discount** | Counterparty *did* issue an opinion on proposition p; how much should it move me on p? | Apply trust discount for competence *on that proposition class* |
| **Out of scope** | Counterparty's verdict is about proposition q ≠ p | They have **no opinion on p** — do not discount a non-opinion to zero; do not fuse it into p |

Zero discount and out-of-scope can produce the same numerical effect on p and still be different reasoning. Only one is right for a given trace. Collapsing them is a category error.

## Operators (v1 surface)

### Trust discounting (scoped competence)

An agent's opinion about a verifier's competence *on a proposition class* discounts that verifier's verdict **on that class** before adoption. Scope-IN (e.g. SchemaPile shape norms) may be high trust; scope-OUT (e.g. external authority codes) may be near-worthless. Discount applies only after proposition scope is established.

### Fusion (v1 restriction)

**v1 restricts licensed fusion operators to: cumulative | averaging | refuse.**

Weighted belief fusion, consensus-and-compromise fusion (CCF), and belief-constraint (Dempster-like) fusion are **out of scope for v1** — not because they are unknown, but because the specimens here are designed around independence failures and proposition-scope errors, where the correct move is often refuse / re-scope rather than constrain. Reviewers should read the restriction as deliberate.

| operator | when licensed |
|----------|----------------|
| **cumulative** | sources are independent given the proposition (evidence adds) |
| **averaging** | sources are dependent or recirculated (do not double-count) |
| **refuse** | fusion is not licensed — different propositions, unresolved dependence, or conflict requiring escalation |

Feedback loops actively produce dependence: dormant hints re-entering a derive round, shared upstream sources, multiple paths through a shared edge, and **selection effects** (an artifact optimized against signal A scored by judge B when A correlates with B). Channel independence (B did not receive A's messages) is **not** object independence (B scores an artifact selected under A).

### Conflict and escalation

When sources assign high b and high d **to the same proposition** (or fused u stays above a stated threshold), no interior membrane can dispose the case — escalation to a higher enclosure is forced. Conflict on misaligned propositions is a scope error, not a fusion input.

### Calibration (metrology)

A measurement is valid only relative to a boundary topology. Stated **u must be licensed by admitted evidence**: u lower than the trace can justify is overconfidence (Goodharting / evaluation-niche leak when evaluation signals cross into the agent niche). Residual u w.r.t. deliberately withheld signals (blind keys) is **correct**; collapsing it without admitting the key is co-adaptation, not better measurement.

## Shared discipline

Treat every label and every cross-participant verdict as a **lossy projection of an opinion relative to a boundary**. Recover the opinion, check proposition scope, then discount or fuse. Every slide back into "the verdict is a fact about p" is an error against this module.
