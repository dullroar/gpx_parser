# DESIGN.md

# GPX Parser Design

## Boundary

This is a small command-line summarizer for GPX route and track files. README.md covers invocation and CSV output; `gpx_parser.py` intentionally contains the complete implementation.

## Core decisions

- Depend only on the Python standard library, using XML parsing and CSV writing directly. The project favors inspectability over a larger GIS dependency stack.
- Normalize output to one summary row per GPX file: route name, endpoints, straight-line distance, and cumulative elevation change.
- Support both tracks and routes while retaining the original GPX namespace-aware parsing approach.
- Accept individual file paths or a directory to make the bundled trail dataset directly usable.

## Constraints

Distance is a haversine calculation between the first and last points, not total trail distance. Elevation gain and loss are simple adjacent-point sums. This is a lightweight summary tool, not a routing, map-matching, or GIS-analysis engine.


