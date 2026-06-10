import xml.etree.ElementTree as ET
import csv
import os
from math import radians, cos, sin, asin, sqrt


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth
    Returns distance in miles
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radius of earth in miles
    r = 3956

    return c * r


def parse_gpx_file(file_path):
    """Parse a GPX file and extract route information"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find the first track or route
        track = root.find(".//{http://www.topografix.com/GPX/1/1}trk")
        route = root.find(".//{http://www.topografix.com/GPX/1/1}rte")
        gpx = root.find(".//{http://www.topografix.com/GPX/1/1}gpx")

        # Get route name
        name = None
        if track is not None:
            name_elem = track.find(".//{http://www.topografix.com/GPX/1/1}name")
            if name_elem is not None:
                name = name_elem.text
        elif route is not None:
            name_elem = route.find(".//{http://www.topografix.com/GPX/1/1}name")
            if name_elem is not None:
                name = name_elem.text
        elif gpx is not None:
            name_elem = gpx.find(".//{http://www.topografix.com/GPX/1/1}name")
            if name_elem is not None:
                name = name_elem.text

        # Extract points from track or route
        points = []

        if track is not None:
            # Look for track segments and points
            segments = track.findall(".//{http://www.topografix.com/GPX/1/1}trkseg")
            for segment in segments:
                for point in segment.findall(
                    ".//{http://www.topografix.com/GPX/1/1}trkpt"
                ):
                    lat = float(point.get("lat"))
                    lon = float(point.get("lon"))
                    points.append((lat, lon))
        elif route is not None:
            # Look for route points
            for point in route.findall(".//{http://www.topografix.com/GPX/1/1}rtept"):
                lat = float(point.get("lat"))
                lon = float(point.get("lon"))
                points.append((lat, lon))

        if not points:
            return None

        # Get start and end points
        start_lat, start_lon = points[0]
        end_lat, end_lon = points[-1]

        # Calculate distance
        distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)

        # Calculate elevation gain and loss
        elevation_gain = 0
        elevation_loss = 0

        # Extract elevation data
        elevations = []

        if track is not None:
            segments = track.findall(".//{http://www.topografix.com/GPX/1/1}trkseg")
            for segment in segments:
                for point in segment.findall(
                    ".//{http://www.topografix.com/GPX/1/1}trkpt"
                ):
                    ele_elem = point.find(".//{http://www.topografix.com/GPX/1/1}ele")
                    if ele_elem is not None and ele_elem.text:
                        elevations.append(float(ele_elem.text))
        elif route is not None:
            for point in route.findall(".//{http://www.topografix.com/GPX/1/1}rtept"):
                ele_elem = point.find(".//{http://www.topografix.com/GPX/1/1}ele")
                if ele_elem is not None and ele_elem.text:
                    elevations.append(float(ele_elem.text))

        # Calculate elevation gain and loss
        if len(elevations) > 1:
            for i in range(1, len(elevations)):
                diff = elevations[i] - elevations[i - 1]
                if diff > 0:
                    elevation_gain += diff
                else:
                    elevation_loss += abs(diff)

        return {
            "file_name": os.path.basename(file_path),
            "route_name": name,
            "start_location": f"{start_lat:.6f}, {start_lon:.6f}",
            "end_location": f"{end_lat:.6f}, {end_lon:.6f}",
            "distance_miles": round(distance, 1),
            "elevation_gain": round(elevation_gain, 1),
            "elevation_loss": round(elevation_loss, 1),
        }

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def process_gpx_files(file_paths, output_csv):
    """Process multiple GPX files and write to CSV"""
    results = []

    for file_path in file_paths:
        if file_path.lower().endswith(".gpx"):
            result = parse_gpx_file(file_path)
            if result:
                results.append(result)

    if not results:
        print("No valid GPX files found or no data extracted.")
        return

    # Write to CSV
    fieldnames = [
        "file_name",
        "route_name",
        "start_location",
        "end_location",
        "distance_miles",
        "elevation_gain",
        "elevation_loss",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(result)

    print(f"Processed {len(results)} GPX files and wrote results to {output_csv}")


def main():
    """Main function to demonstrate usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python gpx_parser.py <gpx_file1.gpx> [gpx_file2.gpx ...]")
        print("Or: python gpx_parser.py <directory_path>")
        return

    files_to_process = []

    # Check if first argument is a directory
    if os.path.isdir(sys.argv[1]):
        directory = sys.argv[1]
        for filename in os.listdir(directory):
            if filename.lower().endswith(".gpx"):
                files_to_process.append(os.path.join(directory, filename))
    else:
        # Process individual files
        files_to_process = sys.argv[1:]

    output_file = "gpx_summary.csv"
    process_gpx_files(files_to_process, output_file)


if __name__ == "__main__":
    main()
