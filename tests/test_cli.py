import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CLI = Path(__file__).resolve().parents[1] / "gpx_parser.py"
COLUMNS = [
    "file_name",
    "route_name",
    "start_location",
    "end_location",
    "distance_miles",
    "elevation_gain",
    "elevation_loss",
]
ROUTE = """\
<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="test">
  <rte>
    <name>Synthetic route</name>
    <rtept lat="0" lon="0"><ele>10</ele></rtept>
    <rtept lat="0" lon="0.5"><ele>35</ele></rtept>
    <rtept lat="0" lon="1"><ele>20</ele></rtept>
  </rte>
</gpx>
"""
TRACK = """\
<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="test">
  <trk>
    <name>Synthetic track</name>
    <trkseg>
      <trkpt lat="0" lon="0"><ele>30</ele></trkpt>
      <trkpt lat="1" lon="0"><ele>10</ele></trkpt>
      <trkpt lat="0" lon="0"><ele>40</ele></trkpt>
    </trkseg>
  </trk>
</gpx>
"""
ROUTE_ROW = ["route.gpx", "Synthetic route", "0.000000, 0.000000",
             "0.000000, 1.000000", "69.0", "25.0", "15.0"]
TRACK_ROW = ["track.GPX", "Synthetic track", "0.000000, 0.000000",
             "0.000000, 0.000000", "0.0", "30.0", "20.0"]


class CliTest(unittest.TestCase):
    def setUp(self):
        self.work_dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.input_dir = self.work_dir / "input"
        self.input_dir.mkdir()
        self.route = self.input_dir / "route.gpx"
        self.route.write_text(ROUTE, encoding="utf-8")
        (self.input_dir / "track.GPX").write_text(TRACK, encoding="utf-8")

    def run_cli(self, *inputs):
        result = subprocess.run(
            [sys.executable, str(CLI), *map(str, inputs)],
            cwd=self.work_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        with (self.work_dir / "gpx_summary.csv").open(newline="", encoding="utf-8") as output:
            rows = list(csv.reader(output))
        self.assertEqual(rows[0], COLUMNS)
        return rows[1:]

    def test_explicit_file(self):
        self.assertEqual(self.run_cli(self.route), [ROUTE_ROW])

    def test_directory(self):
        (self.input_dir / "notes.txt").write_text("Ignore this file.", encoding="utf-8")
        self.assertCountEqual(self.run_cli(self.input_dir), [ROUTE_ROW, TRACK_ROW])
