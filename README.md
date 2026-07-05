# sdg-strategy

**The "how it was made" Data Product** — sibling of [sdg-corpora](https://github.com/zndx/sdg-corpora).
A STRATEGY is the complete, content-addressed answer to *why did the pipeline do that*: every
outcome-shaping determinant that is neither the input window nor the code commit, in four pillars:

| pillar | contents |
|---|---|
| `components/lens/` | the qdrant aperture snapshot (concept ids · labels · vector hashes) |
| `components/voices/` | every agent-facing surface — prompts, schemas, feedback templates, MCP tool docstrings, the vendored vibe writer profile, backend config |
| `components/knobs/` | the flow's tunable defaults |
| `components/targets/` | what it aims at — mined SchemaPile norms (content-hashed), gate floors, the brand lexicon |

## Identity — dual-key, Merkle-shaped

`strategy_id = sha256(sorted component hashes)[:12]` is the **identity** — verifiable by rehash
from any signals project (Atelier, Gaius) with no aegir context. Release tags and zettel ids are
**names**: `sdg-strategy-vX.Y/<zettel-id>`. Component-level references (`targets/…@sha`) resolve
and verify the same way. `manifests/<strategy_id>.json` is the Merkle tree; `CURRENT` names the
checked-out strategy.

## Shadows are branches

- **main lineage = `trunk`** — only it takes release tags (the one-main invariant, mechanically).
- **shadow = a branch** from `trunk@sha`: shared ancestry is the branch point; strategy diff is
  `git diff`; **promotion = cherry-pick** (entry-level) or merge; retirement = archive tag.
- Consumers pin by ref: the aegir submodule pointer tracks main; shadow runs resolve manifests
  **by sha from the object store**, never a working tree.
- Truth flows repo → runtime: live collections are materialized FROM `lens/` snapshots.

## Provenance triple

A run is determined by `(window, strategy, code)`. Corpus run-zettels cite `strategy_id` +
the submodule commit; lineage surfaces (Atlas / OpenLineage) carry the same refs — cache
validity, audit, and cross-project interop are three views of one declaration.

Maintained by the aegir pipeline: `python -m aegir.strategy.manifest {seed|drift}`.
