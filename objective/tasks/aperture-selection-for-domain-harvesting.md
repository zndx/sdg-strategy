# Aperture Selection for Domain Harvesting

## Description:
This task involves reasoning about the choice of Qdrant collection (the "aiming" aperture versus the full vocabulary collection) and the associated strategy lens configuration used to select passages from a large document stream for downstream derivation. It evaluates the model's ability to understand the trade-offs between precision-focused harvesting (tight conceptual aperture) and broader recall, and how the choice of lens snapshot and binding directly shapes the input window for the entire corpus pipeline.

## Modality:
Text only

## Examples:

### Example 1:

Input:

```
A strategy defines two collections:
- aiming collection (sdg_aperture): a smaller, high-precision set of concepts focused on industrial equipment maintenance, failure modes, and sensor readings.
- full vocab collection (sdg_domains): the complete ontology vocabulary.

Explain the expected effect on the harvested passage set and subsequent derive quality if a run uses the aiming collection versus the full vocabulary collection for the initial domain harvest step.
```

Output:
```
Using the aiming collection (sdg_aperture):
- Harvest will be more selective: only passages whose embeddings are close to the aiming concepts will be admitted.
- Expected benefits: higher density of directly relevant content for the target domain (fewer off-topic FinePDFs documents), better signal-to-noise for the derive agent, higher proportion of "rich" metrology outcomes.
- Risks: potential under-coverage of adjacent but useful concepts (e.g., regulatory or supply-chain documents that use broader vocabulary).

Using the full vocabulary collection (sdg_domains):
- Harvest will be broader: any passage matching any domain concept may be included.
- Expected benefits: greater volume and diversity, possibly surfacing useful long-tail patterns.
- Risks: dilution of the input window with marginally relevant material, increased rate of "thin" or "inert" derivations, higher compute cost in later stages, and greater chance that the agent spends rounds on low-value passages.

The choice is recorded in the strategy lens binding and directly influences the harvest cursor and the resulting run zettel. Strategy drift checks will flag changes to the aiming snapshot between runs.
```

---

### Example 2:

Input:

```
During a shadow strategy experiment, the aiming collection snapshot was updated to include additional LIMS and SysML concepts. Describe the likely downstream effects on corpus composition and on the strategy manifest itself.
```

Output:
```
Likely downstream effects:

1. Harvest behavior changes: new passages matching the added LIMS/SysML concepts will now be admitted by the aiming filter that previously would have been excluded.
2. Derive workload shifts: the agent will see more content involving laboratory information management and systems modeling language artifacts. This may increase the rate at which certain ontology families (e.g., measurement, directive) receive new entities.
3. Metrology and congruence scores may move because the new content has different structural characteristics than the original industrial maintenance corpus.
4. The strategy manifest itself must change: the lens/aiming.snapshot.json component will have a new hash, producing a new strategy_id. The lens/aiming.skos.ttl may also be updated.
5. Any run using the new strategy ref will record the updated strategy_id and the corresponding stage_keys in its zettels.
6. When comparing main versus shadow, the difference in aperture is a first-class experimental variable that must be isolated from other strategy changes (voices, targets, etc.).

Because the aiming snapshot is part of the strategy, all such experiments remain fully reproducible and comparable via the manifest.
```

## Tags:
- Aperture Selection
- Information Retrieval
- Harvesting
- Lens Configuration
- Systems Thinking
- Relational Data
- Synthetic