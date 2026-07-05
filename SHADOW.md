# shadow/aperture-r1 — the inaugural shadow (pre-registered as SH-1 in aegir EVIDENCE.md)

**Hypothesis**: extending the AIMING aperture with LIMS / SysML(manufacturing, utility-scale
networks) / CSG(consumer electronics) domain concepts (#73) harvests a materially different
in-domain slice of the SAME FinePDFs window and produces a corpus ≥ main on strategy-neutral
judges.

**To activate**: edit `components/lens/aiming.skos.ttl` (the #73 concept extension), re-seed
component hashes, commit HERE (never trunk). Then:

    uv run --no-sync python -m aegir.strategy.materialize shadow/aperture-r1
    just metaflow --strategy shadow/aperture-r1 --harvest-target 50

The run isolates itself: own corpus dir (`corpus-<strategy_id>/`), own zettel chain,
collections materialized from THIS branch's sources. Compare with:

    uv run --no-sync python -m aegir.clearinghouse.judges <main_corpus> <shadow_corpus>

**Promotion** (per SH-1): ≥3 of 4 mechanical judges AND no rubric regression → cherry-pick
the aiming SKOS delta into trunk (entry-level promotion; the merge commit is the parentage
record). This branch never takes release tags.
