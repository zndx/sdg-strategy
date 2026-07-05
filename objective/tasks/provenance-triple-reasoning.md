# Provenance Triple Reasoning

## Description:
This task requires analyzing or reconstructing the three core determinants of a corpus run — the input window (harvest), the strategy (determinants captured in sdg-strategy), and the code commit — and explaining how specific outcomes (chapter content, construct quality, classification performance, or observed drift) can be attributed to each component. It evaluates the model's ability to perform impact analysis across the provenance triple and to use strategy manifests and run zettels as first-class evidence.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
A new run using the same FinePDFs harvest cursor and the same code commit as a prior run produces noticeably different "rich" versus "thin" ratios and lower overall congruence. The only recorded difference is a new strategy_id. 

Using the structure of a strategy manifest, identify which pillar changes are most likely to explain the shift in metrology outcomes and why.
```

Output:
```
Most diagnostic pillars to inspect:

1. lens/ (especially aiming.snapshot.json and binding.json):
   - A changed aiming snapshot directly alters which passages are harvested even with the same cursor.
   - Different collection names or qdrant_url would cause the derive step to operate over a different conceptual aperture.

2. voices/ (derive.system.md, derive.schema.json, derive.feedback.py, mcp_kvasir.tools.json):
   - Changes here alter the agent's proposal behavior and the exact form of metrology feedback it receives.
   - Updated dormant hints or feedback templates can change how many rounds are spent and what "rich" looks like to the agent.

3. targets/ (schemapile_*_norms.json, floors.json):
   - Updated SchemaPile norms change what kvasir considers structurally good, directly moving the rich/thin threshold.
   - Changed gate floors can cause previously acceptable constructs to be rejected or vice versa.

4. knobs/:
   - Different flow defaults (e.g., passage-chars, rounds, pool) change the operating point of the pipeline even if the underlying voices and targets are similar.

The new strategy_id is the root hash of exactly these component hashes. By comparing the two manifests component-by-component, one can attribute the outcome delta to specific, auditable changes rather than to "the model got lucky."
```

---

### Example 2:

Input:

```
An Atelier blind classification run on a pinned sdg-corpora release shows lower macro-F1 than a previous release on the same held-out columns. The release notes mention only that a new strategy was used for the corpus generation. 

What evidence from the strategy manifest and run zettels would you examine to determine whether the change should be attributed to the strategy versus other factors?
```

Output:
```
Key evidence to examine:

- strategy_id recorded in the new corpus run zettels versus the old ones.
- Full manifest comparison between the two strategy_ids, focusing on:
  - lens/ changes → different passages harvested → different chapters and constructs → different column distributions for classification.
  - voices/aegir_writer.md or register_voice.json → changed prose style may affect how clearly table semantics are described, impacting blind classifiers that use chapter text.
  - targets/ (brand_lexicon, floors) → changes here can alter which entities are admitted or how congruence is computed, indirectly affecting the quality of the released vocabulary and constructs.
- Per-stage lineage keys (from strategy/lineage.py) for "harvest", "derive", "realize", "prose", and "congruence". A change isolated to the harvest stage key strongly implicates the lens.
- The actual corpus_columns.parquet or base_rows for the two releases to see whether the set of blind columns or their value distributions shifted.

If the strategy change is confined to voices/aegir_writer.md with no lens or target movement, the performance drop is more likely attributable to description quality than to a fundamentally different relational substrate.
```

## Tags:
- Provenance
- Strategy Manifest
- Impact Analysis
- Reproducibility
- Critical Thinking
- Relational Data
- Synthetic