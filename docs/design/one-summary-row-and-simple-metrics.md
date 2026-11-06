---
gist: "Read when: changing the CSV output columns, the distance or elevation calculations, or route/track handling."
---

# One summary row per file, simple metrics

**Decision.** Output is normalized to one row per GPX file: route name, endpoints, straight-line distance, and cumulative elevation change. Tracks and routes are both supported with namespace-aware parsing.

**Limits to keep visible.** Distance is a haversine calculation between the first and last points, not total trail distance. Elevation gain and loss are simple adjacent-point sums. Changing either is a behavior change, not a cleanup.
