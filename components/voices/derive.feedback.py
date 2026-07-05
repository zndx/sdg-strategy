def _feedback(signal: dict) -> str:  # noqa: D103 — see _dormant_brief below
    """The membrane's reason, framed as re-prompt context for the next proposal round."""
    y = signal.get("ddl_yield") or {}
    return (
        "Your previous schema draft was profiled against real-world database norms "
        f"(verdict: {signal.get('verdict')}). Measured: {y.get('n_elected', 0)} entity tables, "
        f"{y.get('n_junctions', 0)} junction tables, {y.get('n_lookups', 0)} lookup tables, "
        f"attribute-less-class ratio {y.get('attr_zero_ratio', 1.0):.2f}, median width "
        f"{y.get('width_median', 0)}. {signal.get('reason', '')} "
        "Revise: keep the same subject-matter entities but deepen them — more typed attributes "
        "per entity (dates, quantities, codes, booleans), closed value sets (enum) where the "
        "passage implies categories, and cardinality-bounded relations between entities. "
        "Model the passage's OWN domain; do not invent unrelated entities."
        + _dormant_brief(signal)
    )
def _dormant_brief(signal: dict) -> str:
    dormant = [d for d in (signal.get("dormant_paths") or []) if d in _DORMANT_HINTS]
    if not dormant:
        return ""
    wants = "; ".join(_DORMANT_HINTS[d] for d in dormant[:4])
    return (" Structural coverage note: this draft exercises none of the following real-world "
            f"schema patterns — {wants}. If the domain PLAUSIBLY carries any of them, model "
            "them; interesting structure is welcome where the subject matter supports it.")
