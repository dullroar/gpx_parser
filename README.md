# GPX Parser

For calculation boundaries and implementation decisions, see [docs/design/](docs/design/README.md).

A command-line tool that batch-processes GPX files and summarizes each route's key statistics into a single CSV file.

## Features

- Parses GPX 1.1 files containing either track (`<trk>`) or route (`<rte>`) data
- Extracts route name, start/end coordinates, straight-line distance, and cumulative elevation gain/loss
- Accepts individual files or an entire directory as input
- Outputs a single consolidated CSV file
- No third-party dependencies — uses Python standard library only

## Requirements

- Python 3.x

## Usage

**Process individual files:**
```bash
python gpx_parser.py file1.gpx file2.gpx file3.gpx
```

**Process all GPX files in a directory:**
```bash
python gpx_parser.py /path/to/gpx/folder
```

Output is written to `gpx_summary.csv` in the current working directory.

## Output Format

The CSV contains one row per GPX file with the following columns:

| Column | Description | Units |
|---|---|---|
| `file_name` | Source GPX filename | — |
| `route_name` | Route name from the GPX `<name>` element | — |
| `start_location` | Latitude, longitude of the first point | decimal degrees |
| `end_location` | Latitude, longitude of the last point | decimal degrees |
| `distance_miles` | Straight-line (haversine) distance from start to end | miles |
| `elevation_gain` | Cumulative elevation gain along the route | meters |
| `elevation_loss` | Cumulative elevation loss along the route | meters |

> **Note:** `distance_miles` is the straight-line displacement between the start and end points, not the total trail distance traveled.
> Elevation gain and loss are in **meters**, as stored in the GPX `<ele>` elements.

### Example output (`gpx_summary.csv`)

```
file_name,route_name,start_location,end_location,distance_miles,elevation_gain,elevation_loss
td01s1d1-grape-cr-to-cottonwood-cr.gpx,TD01:S1:D1 Grape Cr to Cottonwood Cr,"37.931098, -105.457566","38.066779, -105.556629",10.8,1175.8,1109.0
td02s1d2-cottonwood-cr-to-goat-cr.gpx,TD02:S1:D2 Cottonwood Cr to Goat Cr,"38.065623, -105.555879","38.190284, -105.629770",9.5,1165.2,1238.0
```

## Implementation notes

The parser's track/route selection and calculation boundaries are documented in
[docs/design/](docs/design/README.md).

## Docker build and tests

Use Bash and a running Docker engine that can build and run Linux containers.
The build can pull the Python base image. The tests use synthetic GPX files
and run with the container network disabled.

```bash
docker build -t gpx-parser:test .
bash scripts/test_docker.sh
```

The test script builds a temporary image from the current checkout. It runs
the CLI tests and context checks as a normal container user, then removes the
temporary image. To run the CLI tests directly on the host, use
`python3 -m unittest discover -s tests -v` with Python 3.11 or later.

To run the [migration plan](plans/ralphify/plan.md) with
[ralph-looper](https://github.com/dullroar/ralph-looper), run this command from
the repository with Ralph Looper and Codex on your path.

```bash
ralph-looper --repo . --plan ralphify --agent codex
```

## Sample Dataset

The included GPX files are 30 day-segments of a long route through southern Colorado, labeled with a `TD##:S#:D#` naming convention (Trail Day : Segment : Day). The route runs roughly from Grape Creek near Salida south to Cumbres Pass, covering terrain in the San Juan Mountains and Rio Grande National Forest.
