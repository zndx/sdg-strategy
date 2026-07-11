# Aperture Selection for Domain Harvesting

## Description:
This task requires designing, predicting, and auditing a **harvest aperture**: the admission membrane that selects which passages from a raw document stream enter downstream derivation and evaluation. Answers must rest on **computable ground truth** (simulator counts, cost arithmetic, set identities) and state confirming probes. Narrative trade-off essays without numbers or set reasoning do not complete the task.

> Choose or diagnose a boundary topology `(C, regime params, e, index)` over a document stream, knowing every downstream measurement is conditional on what that membrane admits. Recover admitted-set composition, operating points under stated costs, which cross-aperture comparisons are licensed, whether observed drift is membrane-move or stream-move, and what the aperture structurally cannot admit.

### Aperture (membrane)

An **aperture** admits or rejects passages (or analogous units). Distinguish:

- **Window** — the raw slice of material available (cursor, snapshot, corpus epoch) before selection.
- **Aperture** — the selection mechanism applied to that window.

**Score.** In the reference text setting, passages and concepts are encoded as ColBERT multi-vectors; `sim(e(p), e(c))` denotes **MaxSim** (late-interaction maximum similarity) of those multi-vectors, as implemented by multivector indexes that expose MaxSim (e.g. Qdrant `MAX_SIM`). Scoring uses concept **definitional text** (labels plus definitions and scope notes): richer definitional content strengthens MaxSim against real documents. When a specimen writes `sim`, it means this MaxSim unless it names another scorer.

**Admission regime** (declare per specimen; the two have different theorems):

| regime | rule | monotonicity in C |
|--------|------|-------------------|
| **threshold** | `admit(p) ⇔ ∃ c ∈ C. MaxSim(e(p), e(c)) ≥ τ` | **Monotone:** C ⊆ C′ ⇒ A(C) ⊆ A(C′). Intersection A ∩ A′ = A when C ⊆ C′. |
| **top-k / budget** | s(p) = max_{c∈C} MaxSim(e(p), e(c)); admit the top k (or fill budget B), optionally requiring s(p) ≥ τ_floor | **Non-monotone:** enlarging C re-ranks the pool; previously admitted passages can be **evicted**. \|A\| may be fixed by construction. |

Every specimen must state its regime. Unmarked regime is a defect. “Adding concepts only grows the set” holds under threshold; under budget it is a trap.

| component | role | pin for reproducible harvest |
|-----------|------|------------------------------|
| **C** | concept set (e.g. SKOS aiming concepts → multivector points) | content-addressed concept snapshot / SKOS source |
| **τ / k / B** | threshold and/or top-k budget / floor | harvest policy parameters |
| **e** | multi-vector encoder model version | model id + weights digest |
| **index** | ANN realization (HNSW ef/M, quantization) or exact MaxSim | index params in the identity hash, or exact search at the gate |

**Effective aperture** = `(C, regime params, e, index)`. Identity hashes that omit `e` or `index` can label two different membranes as equal.

Typical concept sets: a small **aiming** aperture (domain-focused concepts with rich definitions) versus a large **vocabulary** collection (broad classification vocabulary; often used for later grounding/congruence rather than as the harvest rifle). **Composite** aiming may union vertical domains (laboratory, manufacturing, energy, geometry, utility, …) with horizontal data-engineering concepts (schema, lineage, catalog, quality).

### Ground truth

Specimens supply (or imply) a **labeled stream simulator**: domain labels per passage, MaxSim or rank tables against C, and optional post-admission outcome class (`rich` / `thin` / inert).

| quantity | nature |
|----------|--------|
| admitted set A, \|A\| | count |
| precision / recall / adjacent coverage | count ratios |
| composition over domain labels | counts; optional opinion masses with uncertainty licensed by sample size |
| base rates a(·) for composition opinions | **stream composition** (or another stated frame prior) |
| operating value under a cost model | arithmetic on counts |

**Cost model** (required when asking which aperture is better):

- `c_pass` — cost per harvested passage through derive  
- `v_rich` — value of a rich derivation  
- `c_thin` — cost of a thin/inert round  
- optional `c_miss` — cost of missing a valuable in-domain passage  

Without a cost model (or another stated objective), “better” is **underdetermined**; the correct answer states what must be specified.

### Selection effects and comparability

**Rich-rate conditioned on admission is not comparable across apertures** as a population-invariant quality claim: tightening C or raising τ changes the measured population. Cross-aperture metric comparison is licensed only via:

| correction | meaning | regime note |
|------------|---------|-------------|
| **(a) Intersection** | evaluate only on A₁ ∩ A₂ | Exact under threshold when sets nest; under budget, intersection may be a strict subset of both (evictions)—still valid on shared passages, prefer (b) when studying eviction |
| **(b) Fixed probe set** | canaries / holdout scored under every membrane | Regime-safe |
| **(c) Importance weighting** | reweight by admission propensities | Requires a propensity model |

Raw rich-rate or mix-rate comparison without (a)–(c) is incorrect.

### Question types

| code | type | ask |
|------|------|-----|
| **O** | operating-point selection | stream stats + costs → choose C / τ / k; value computable |
| **M** | composition prediction | admitted makeup (counts or opinions); a(·) from stream prior when numeric |
| **X** | comparability analysis | which cross-aperture comparisons are licensed; name (a)/(b)/(c) or refuse |
| **D** | drift attribution | membrane moved vs stream moved (may be **underdetermined**) |
| **B** | blind-spot reasoning | what the aperture cannot admit; canary probes |
| **H** | membrane completeness | whether identity pins full `(C, regime, e, index)` |

Composite answers are expected where appropriate.

### Required output shape

```
Membrane: regime=threshold|top-k/budget  C=…  τ/k/B=…  e=…  index=…   [or incomplete pin]
Verdict classes: <O|M|X|D|B|H …>

Admitted-set / composition (counts or opinions; uncertainty licensed if predictive):
  …

Operating value (if O):  V = …   [show arithmetic]

Comparability (if X or any cross-aperture metric claim):
  licensed: yes via (a|b|c) | no — refuse naive comparison

Drift (if D):
  membrane | stream | underdetermined
  fingerprint: …

Blind spots / canaries (if B):
  …

Confirming probe: <re-harvest, pin change, canary injection, or intersection eval>
```

Derivation must cite simulator tables, manifests, and cost numbers.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
Harvest membrane choice. Regime: **threshold** (admit iff max_c sim ≥ τ). Stream simulator (N = 10_000 passages, labels known).

Stream composition (also the pinned frame prior a(·) if an M-class opinion over domain labels is emitted):
- LIMS-core: 800  (a=0.08)
- DATAENG (schema/lineage/catalog prose): 600  (a=0.06)
- adjacent (regulatory / supply-chain touching labs): 1_200  (a=0.12)
- off-domain: 7_400  (a=0.74)

Two candidate membranes (same e = colbert-v1@sha_e1, exact search):

Membrane A — aiming C_A = {LIMS concepts with rich skos:definition text}, τ = 0.62
  Simulator admission counts: LIMS 640, DATAENG 40, adjacent 180, off 90  → |A| = 950
  Of admitted, derive outcomes if run: rich 380, thin 420, inert 150

Membrane V — binding uses full vocab C_V = sdg_domains (973 concepts), same τ = 0.62, same e
  Note: C_V entries carry definitional/example text (often thinner and more heterogeneous than aiming's domain definitions). Combined with |C_V| ≫ |C_A|, MaxSim can clear τ for more LIMS-tagged passages under V than under A. Content-first scoring still uses definitional text; a zero-definition label litany is a separate canary case (see Example 5, K5).
  Admission: LIMS 700, DATAENG 420, adjacent 900, off 2_100 → |A| = 4_120
  Outcomes: rich 520, thin 2_400, inert 1_200

Cost model: c_pass = 1, v_rich = 5, c_thin = 1 (inert charged as thin). No separate c_miss.

Tasks:
1. Compute operating value V = v_rich·n_rich − c_pass·|A| − c_thin·(n_thin+n_inert) for A and V. Which wins under this cost model?
2. Compare "rich rate" rich/|A| across membranes. Is the comparison licensed? If not, what correction applies?
3. Stage role: is V an appropriate *harvest* aperture, or a mis-bound congruence vocabulary?
```

Output:
```
Membrane: regime=threshold; A = (C_LIMS, τ=0.62, e=colbert-v1@sha_e1, exact); V = (C_vocab, same τ, e, exact)
Verdict classes: **O + X + H/stage**

1. Operating values:
   V_A = 5·380 − 1·950 − 1·(420+150) = 1900 − 950 − 570 = **380**
   V_V = 5·520 − 1·4120 − 1·(2400+1200) = 2600 − 4120 − 3600 = **−5120**
   Under this cost model **A wins**. (Different costs could flip O; the fact of the matter is the arithmetic, not an essay.)

2. Rich rates: A → 380/950 ≈ 0.40; V → 520/4120 ≈ 0.13.
   **Naive comparison of rich-rate across A and V is not licensed** as proof that A "produces higher quality derivations" in a population-invariant sense — the rate is conditioned on different admission events (selection effect / channel≠object in retrieval costume).
   Licensed options under threshold:
   - (a) evaluate outcomes only on A ∩ V (exact here; A need not nest in V because C_A ⊈ C_V as concept *sets* even if both hit LIMS-labeled passages);
   - (b) fixed probe set run under both membranes;
   - (c) importance weights if propensities are modeled.
   Raw rich-rate improvement under A is partly **population change**, not only better work on shared passages.

3. Stage role: full vocab as harvest aperture is usually a **mis-binding** for this pipeline: its primary role is later congruence/grounding; as harvest C it admits heavy off-domain mass (2100) while still, via cardinality and residual definitions, admitting more LIMS-tagged text than tight aiming. H: binding must declare which collection is the harvest aperture.

Confirming probe: score the same 200 labeled canaries under A and V (correction b); recompute rich-rate and V on that fixed set. If A's advantage shrinks to near zero on the intersection/probe while remaining large on conditioned rates, the selection artifact is confirmed.
```

---

### Example 2:

Input:

```
Operating-point selection on τ only. Regime: **threshold**. Fixed C = composite aiming (LIMS + manufacturing + energy + CSG + utility + DATAENG; 29 concepts), e and exact search pinned.

Simulator gives admission and outcome counts vs τ:

τ     |A|   n_rich  n_thin+inert  n_in_domain_missed (of 2000 in-domain in stream)
0.50  2400  420     1980          200
0.62  1100  360     740           480
0.75   500  280     220           900

Cost model: c_pass = 1, v_rich = 4, c_thin = 1, c_miss = 2
Define V(τ) = v_rich·n_rich − c_pass·|A| − c_thin·(n_thin+inert) − c_miss·n_in_domain_missed

Also define the abstention baseline: harvest nothing ⇒ |A|=0, n_rich=0, n_thin=0, n_missed=2000 → V(∅) = −c_miss·2000.

Select τ*. Show arithmetic including V(∅). State what remains underdetermined if c_miss were unspecified — and how sharp the 0.62 vs 0.75 margin is at c_miss = 2.
```

Output:
```
Membrane: regime=threshold; C fixed composite aiming; e pinned; exact; τ varies
Verdict classes: **O**

V(0.50) = 4·420 − 2400 − 1980 − 2·200 = 1680 − 2400 − 1980 − 400 = **−3100**
V(0.62) = 4·360 − 1100 − 740 − 2·480 = 1440 − 1100 − 740 − 960 = **−1360**
V(0.75) = 4·280 − 500 − 220 − 2·900 = 1120 − 500 − 220 − 1800 = **−1400**
V(∅)    = −2·2000 = **−4000**

τ* = **0.62** under this cost model: best among tabulated τ and **beats abstention** (−1360 > −4000). Negative V means the stated prices still prefer running at 0.62 over not harvesting; "all grid points negative" is not a license to abstain without comparing V(∅).

Knife-edge (deliberate): V(0.62) − V(0.75) = 40 at c_miss = 2. Equating V(0.62)=V(0.75):
  (−400 − 480 c) = (400 − 900 c)  ⇒  420 c = 800  ⇒  c_miss* = 800/420 ≈ **1.90**.
So 0.62 beats 0.75 only for c_miss > ≈1.90; the specimen is built so the ranking is thin at the stated c_miss = 2 — making underdetermination-without-c_miss vivid, not accidental.

If c_miss were unspecified: ranking between 0.62 and 0.75 is **underdetermined** (crosses at ≈1.90); correct output is underdetermination + request for c_miss (or a probe-set recall SLA), not a preferred essay.

Confirming probe: denser τ grid around 0.62; or hold τ and expand C (DATAENG definitions) to reduce misses without lowering τ — tests C–τ edge.
```

---

### Example 3:

Input:

```
Shadow experiment under **top-k / budget** admission (not pure threshold).

Regime: score s(p) = max_c sim(e(p), e(c)); admit the top **k = 1000** passages with s(p) ≥ τ_floor = 0.50 (fill budget from the ranked pool). Same e, exact search, same window W.

Main strategy_id S0 pins aiming C0 (no DATAENG branch). Shadow S1 adds DATAENG concepts (notation 14.x) to aiming SKOS; new aiming.snapshot hash → new strategy_id S1. Voices/targets unchanged.

Simulator (same W):
- Main A0: |A0| = 1000 (budget-full); domain mix: LIMS 55%, mfg 20%, energy 10%, other-vertical 10%, DATAENG-labeled 5%
  rich-rate on A0: 0.38
- Shadow A1: |A1| = 1000 (budget-full); mix: LIMS 48%, mfg 17%, energy 8%, other-vertical 8%, DATAENG-labeled 19%
  rich-rate on A1: 0.31
- Intersection |A0 ∩ A1| = 920  (80 passages in A0 were **evicted** under S1: re-ranked below the budget cut by new DATAENG-strong competitors; 80 new DATAENG-heavy passages entered)
- Rich-rate on intersection under main derive config: 0.37; under shadow re-derive on same 920: 0.36
- Evicted set E = A0 \ A1 (80): rich-rate was 0.50 under main (higher than A0 average — eviction is not random)
- Entered set N = A1 \ A0 (80): rich-rate 0.15 under shadow

A colleague claims: "Shadow is worse — rich-rate dropped from 0.38 to 0.31; roll back DATAENG."

Assess regime consequences (monotonicity), composition, manifest identity, and whether the colleague's comparison is licensed. Note what intersection correction (a) does and does not mean under budget.
```

Output:
```
Membrane: regime=**top-k/budget** k=1000, τ_floor=0.50; S0=(C0,…); S1=(C0∪DATAENG,…); e, index, W pinned
Verdict classes: **M + X + H**

Regime / monotonicity:
- Under threshold, C0 ⊆ C1 ⇒ A0 ⊆ A1 and |A0 ∩ A1| = |A0|. Here |A0 ∩ A1| = 920 < 1000 = |A0| is **impossible under threshold** but **expected under budget**: adding DATAENG re-ranks the pool and **evicts** 80 previously admitted passages. Eviction-under-budget is the trap (intuition says adding concepts only grows the set).
- Fixed |A|=1000 both runs is by construction of k, not a coincidence.

Manifest / H:
- S0 → S1 correctly rolls strategy_id via aiming.skos + snapshot hashes. Voices unchanged ⇒ harvest delta attributable to C under the stated budget regime.

Composition (M):
- DATAENG-labeled share 5% → 19% at fixed |A|; LIMS share 55% → 48% is mix shift from re-ranking, not proof LIMS vanished. Stream composition remains the pinned a(·) if emitting ω over labels; admitted mix is the posterior counts, not a new silent prior.
- Evicted E was *richer* (0.50) than entered N (0.15) — budget + DATAENG can trade high-value old admits for low-value new admits; that is an O-relevant cost fact once valued, not only an M fact.

Comparability (X):
- Colleague's raw 0.38 → 0.31: **not licensed** (different populations; selection effect).
- Intersection (a) on 920 shared passages: 0.37 vs 0.36 — negligible quality change on survivors. Under budget, (a) licenses comparison **only on the non-evicted core**; it does **not** equal "evaluate the old A0 nested inside A1" (A0 ⊈ A1). The eviction set E and entry set N must be reported separately or the story is incomplete.
- Prefer (b) fixed probe set when eviction itself is under test.
- Do not roll back DATAENG on naive rich-rate alone; if rollback is argued, it must be from V on E∪N or probe canaries, not conditioned rates on A0 vs A1.

Confirming probe:
1. Re-run S1 under **threshold** regime with no k cap (same τ_floor or a pure τ): expect A0 ⊆ A1' and intersection = A0 if C only grew — confirms the non-nesting was regime-driven.
2. Probe set (b): LIMS / DATAENG / off-domain canaries under S0 and S1.
3. Score E and N under a fixed derive config; if E's value exceeds N's by more than the DATAENG coverage gain is worth under the cost model, O favors a hybrid (DATAENG in C but higher τ_floor or reserved budget slots).
```

---

### Example 4:

Input:

```
Drift attribution. Two harvest runs, same declared strategy_id S (byte-identical lens/aiming.snapshot.json, binding, knobs, recorded e digest, exact search).

Regime: **top-k / budget** with k = 1200 (τ_floor pinned). Window pins differ:

Run 0: FinePDFs cursor epoch E0 → admitted composition: LIMS 50%, energy 25%, DATAENG 15%, off 10%; |A|=1200
Run 1: cursor epoch E1 (three months later) → LIMS 35%, energy 20%, DATAENG 15%, off 30%; |A|=1200

No re-materialize between runs. ANN set to exact in both.

A dashboard flags "aperture drift" because off-domain share rose.

Attribute: membrane vs stream vs underdetermined. What fingerprint distinguishes the cases? Why is |A| identical not evidence of a frozen stream?
```

Output:
```
Membrane: regime=top-k/budget k=1200; claimed identical S (C, τ_floor, e, exact) both runs
Verdict classes: **D**

Attribution: **stream-primary** (window / source distribution moved), not membrane-move — *given* the manifest pins are trusted and exact search eliminates index nondeterminism.

Fingerprint:
- Membrane-move: concept/threshold/budget/model/index hash changes; admission deltas **align to edited concepts** (category-structured around C diff) even on a frozen stream replay.
- Stream-move: strategy_id and membrane pins unchanged; composition tracks **source mix / cursor epoch**; replaying Run1's membrane on E0's frozen passages recovers Run0-like mix.
- Here strategy_id and e/τ_floor/C/k are identical by statement ⇒ membrane-move is eliminated unless H fails (undeclared e/index drift). Off-domain rise with fixed membrane is the signature of a moving FinePDFs distribution — **exactly what snapshot hashes will not flag**.

|A|=1200 both runs is **not** evidence the stream froze: under budget regime |A|=k **by construction**. Under pure threshold, identical |A| across a large stream shift would be a coincidence worth checking; here it is expected. (Regime declaration prevents that misread.)

If e or ANN were **not** in the pin set: **underdetermined** between silent membrane change and stream change — correct verdict U + probe, not a guess.

Confirming probe:
1. Re-harvest E0 passages with Run1 binary/config; expect Run0 composition if membrane truly fixed.
2. Re-harvest E1 with Run0 config; expect Run1-like off-domain elevation if stream moved.
3. If (1) fails, hunt undeclared e/index drift (H defect) despite strategy_id equality.
```

---

### Example 5:

Input:

```
Blind-spot / canary design. Regime: **threshold**. Composite aiming C includes LIMS + DATAENG with rich skos:definition text; τ = 0.62; e pinned; exact search.

Claim by author: "Aperture covers laboratory results end-to-end including column-semantic cataloging."

Available canary passages (labels known, sim-to-nearest-c tabulated offline against this C):

| id | label | max sim to C | notes |
|----|-------|--------------|-------|
| K1 | LIMS specimen lifecycle | 0.81 | should admit |
| K2 | DATAENG column semantic type annotation | 0.78 | should admit if DATAENG definitions are real |
| K3 | pure tax-code jurisdiction essay | 0.41 | off-domain |
| K4 | LIMS-adjacent GLP regulation without assay content | 0.58 | adjacent; borderline |
| K5 | vocab-label litany only ("Customer, Order, Amount") with no definitional prose | 0.44 | tests content-first doctrine |
| K6 | well-log WITSML trajectory narrative | 0.33 | energy not in this C (C is LIMS+DATAENG only for this specimen) |

τ = 0.62. Which canaries must admit / must reject if the claim and content-first doctrine hold? What does a K2 miss falsify? Verdict class B.
```

Output:
```
Membrane: regime=threshold; C = LIMS ∪ DATAENG; τ=0.62; e pinned; exact
Verdict classes: **B** (+ doctrine check)

Admission under claim + τ:
- **Must admit:** K1 (0.81), K2 (0.78) — in-domain for stated C; K2 is the dogfood canary for "column-semantic cataloging."
- **Must reject:** K3 (0.41), K5 (0.44), K6 (0.33) — below τ; K6 is structural blind spot for this C (energy not in membrane); K5 fails content-first (labels without definitions should not clear a definition-driven MaxSim gate).
- **Borderline:** K4 (0.58) — reject at 0.62; adjacent coverage is a conscious blind spot unless τ or C expands.

If K2 misses (sim actually < τ or not in index): falsifies "cataloging covered" — either DATAENG definitions are poor/empty (separation failure), wrong collection binding, or index not materialized from claimed SKOS (H/materialize defect).

K5 is the zero-definition litany canary. A large vocabulary collection whose entries still carry definitional text can clear τ for many passages; that case is cardinality-plus-definitions, distinct from K5.

Confirming probe: inject K1–K6 into the live stream (or offline MaxSim table against production C); require the admit/reject pattern above. Expanding C to energy should flip K6 without flipping K3.
```

---

### Example 6:

Input:

```
Membrane completeness (H). Two runs report the same strategy_id S from hashing:
  lens/aiming.skos.ttl, aiming.snapshot.json, binding.json, knobs (τ=0.62, and k if budget), voices, targets.

Regime claimed: threshold τ=0.62 (but see below).

Run R0 and R1 use different embedding image digests (e0 vs e1) not present in the manifest leaves.
Both use HNSW with ef=64 on R0 and ef=256 on R1; neither ef nor "exact vs ANN" is hashed.
Realized |A| and top-domain mix differ substantially on the same window pin W.

Is strategy_id equality sufficient to treat apertures as identical? What must be pinned? How does this interact with drift checks?
```

Output:
```
Membrane: regime claimed threshold; nominal S identical; effective (C, τ, e, index) **not** identical
Verdict classes: **H + D**

strategy_id equality is **not** sufficient. Effective aperture = (C, regime params, e, index). Here e and ANN params moved outside the hash ⇒ **hidden membrane components**. Realized admission differences on fixed W are membrane-effective drift invisible to current drift checks.

Must pin for metrology-grade harvest:
- e: model id + weights/image digest
- index: exact search **or** (HNSW M/ef, quantization, build seed) in the manifest / stage_key
- regime: threshold vs top-k/budget, and k/B/τ_floor as applicable
- C, τ already partially pinned via lens + knobs

Until then: two runs with same strategy_id can harvest different sets — gate defect, not stream mystery.

Drift interaction: dashboard "composition drift" under same strategy_id is **underdetermined** among (stream move | silent e change | ANN recall change | silent regime param change). Confirming probes must freeze W and swap one factor at a time.

Confirming probe:
1. Mandate exact search at harvest gate (or hash ef/M); re-run R0/R1 on W.
2. Add e digest to strategy leaves; expect strategy_id split when e0≠e1.
3. Replay identical (C, regime params, e, exact) on W — admitted sets should match within tie-break policy.
```

## Tags:
- Aperture Selection
- Information Retrieval
- Late Interaction
- MaxSim
- Operating Point
- Selection Effects
- Experimental Design
- Drift Attribution
- Metrology
- Systems Thinking
- Synthetic
