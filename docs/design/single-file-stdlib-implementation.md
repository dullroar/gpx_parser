---
gist: "Read when: adding a dependency, splitting gpx_parser.py into modules, or changing how input paths and directories are accepted."
---

# Single-file, standard-library implementation

**Decision.** `gpx_parser.py` intentionally contains the complete implementation and depends only on the Python standard library (XML parsing and CSV writing), favoring inspectability over a larger GIS dependency stack. It accepts individual file paths or a directory so the bundled trail dataset is directly usable.

**Boundary.** A lightweight summary tool, not a routing, map-matching, or GIS-analysis engine.
