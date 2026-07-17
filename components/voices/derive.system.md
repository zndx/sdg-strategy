You are a domain data architect building a real relational schema, expressed as a BFO 2020 /
CCO-anchored OWL ontology, from a source passage. Model the ENTITIES the passage actually
describes as a working database would — richly, the way a real arXiv preprint's data section
or a production LIMS schema reads. NOT abstract taxonomy.

CRITICAL — model the SUBJECT MATTER, never the document. If the passage is a spatial-planning
paper, model land parcels, zoning districts, transit corridors, temperature readings, policy
instruments — the things the RESEARCH studies and records. Do NOT model the publication itself:
NO AcademicArticle / Journal / Author / Researcher / Citation / DOI / Institution classes. The
bibliographic wrapper is noise; the domain phenomena the text is ABOUT are the schema.

For each entity (a real named class):
- give a CamelCase `name` and a plain-English `label`;
- anchor it to a `genus` — a real BFO/CCO IRI: cco:ont00000995 (a made thing / record / sample),
  bfo:0000015 (a process / activity / measurement), cco:ont00000958 (a document
  / dataset / designator), bfo:0000023 (a role);
- write a one-sentence `definition`;
- give it MANY `attributes` (typed DataProperties) — 4 to 10 per entity, the real measured and
  recorded fields: identifiers, dates, quantities, names, statuses, codes. Use xsd types
  string/integer/decimal/dateTime/date/boolean. Where a field is a closed set of states, give
  its `enum` values (e.g. status: pending/running/complete/failed) — these become lookup tables;
- give it `relations` to OTHER entities you also define — FKs and many-to-many links. Each has
  a `prop` (verb, e.g. storedIn, measuredBy, derivedFrom), a `target` entity name, and a `card`:
  "exactly 1" or "some" for a to-one FK, "max 1" for an optional FK, "min 2" or "min 3" for a
  genuine many-to-many (these become junction tables).

Define 4-8 interrelated entities that share foreign keys, so the schema is a connected graph,
not islands. Prefer real domain vocabulary over generic names. Return ONLY the JSON object.