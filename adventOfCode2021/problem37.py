import math
import sys
from typing import List, Set, Optional, Tuple, Dict


directions = [
    (0, 1, 2, 1, 1, 1),
    (0, 2, 1, 1, 1, -1),
    (0, 1, 2, 1, -1, -1),
    (0, 2, 1, 1, -1, 1),
    (0, 1, 2, -1, 1, -1),
    (0, 2, 1, -1, 1, 1),
    (0, 1, 2, -1, -1, 1),
    (0, 2, 1, -1, -1, -1),
    (1, 0, 2, 1, 1, -1),
    (1, 2, 0, 1, -1, -1),
    (1, 0, 2, 1, -1, 1),
    (1, 2, 0, 1, 1, 1),
    (1, 0, 2, -1, 1, 1),
    (1, 2, 0, -1, 1, -1),
    (1, 0, 2, -1, -1, -1),
    (1, 2, 0, -1, -1, 1),
    (2, 1, 0, 1, 1, -1),
    (2, 0, 1, 1, -1, -1),
    (2, 1, 0, 1, -1, 1),
    (2, 0, 1, 1, 1, 1),
    (2, 1, 0, -1, 1, 1),
    (2, 0, 1, -1, 1, -1),
    (2, 1, 0, -1, -1, -1),
    (2, 0, 1, -1, -1, 1),
]


def rotate_position(coordinates: Tuple[int, int, int], direction: List[int]) -> Tuple[int, int, int]:
    x_index, y_index, z_index, x_multiplier, y_multiplier, z_multiplier = direction
    return coordinates[x_index] * x_multiplier, coordinates[y_index] * y_multiplier, coordinates[z_index] * z_multiplier


def get_all_coordinate_rotations(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    coordinates = [x, y, z]
    return [
        (coordinates[x_index] * x_multiplier, coordinates[y_index] * y_multiplier, coordinates[z_index] * z_multiplier)
        for (x_index, y_index, z_index, x_multiplier, y_multiplier, z_multiplier) in directions
    ]


def build_distances_map(scanner: List[Tuple[int, int, int]]) -> List[List[int]]:
    distances_map = []
    for beacon in scanner:
        distances_map.append([])
        for other_beacon in scanner:
            distances_map[-1].append(
                math.sqrt((beacon[0] - other_beacon[0]) ** 2 + (beacon[1] - other_beacon[1]) ** 2 + (beacon[2] - other_beacon[2]) ** 2)
            )
    return distances_map


def find_overlapping(
        first_scanner_distances: List[List[int]],
        second_scanner_distances: List[List[int]],
        debugging: bool
) -> Optional[List[Tuple[int, int]]]:
    matches = None
    distances_with_matches = None
    for first_scanner_beacon_distances in first_scanner_distances:
        for second_scanner_beacon_distances in second_scanner_distances:
            common_distances = set(first_scanner_beacon_distances).intersection(set(second_scanner_beacon_distances))
            if debugging:
                print(first_scanner_beacon_distances, second_scanner_beacon_distances)
            if len(common_distances) == 12:
                matches = common_distances
                distances_with_matches = (first_scanner_beacon_distances, second_scanner_beacon_distances)
                break
        if matches is not None:
            break

    if matches is None or distances_with_matches is None:
        return None

    result = []
    first_scanner_beacon_distances, second_scanner_beacon_distances = distances_with_matches
    for (i, first_scanner_beacon_distance) in enumerate(first_scanner_beacon_distances):
        if first_scanner_beacon_distance in matches:
            j = second_scanner_beacon_distances.index(first_scanner_beacon_distance)
            result.append((i, j))
    return result


def get_scanner_pairs(scanner_maps: List[List[List[int]]]) -> Dict[int, Tuple[int, List[Tuple[int, int]]]]:
    scanner_pairs = {}
    for (i, first_scanner_map) in enumerate(scanner_maps):
        for (j, second_scanner_map) in enumerate(scanner_maps):
            if i == j:
                continue
            overlapping_result = find_overlapping(first_scanner_map, second_scanner_map, False)
            if overlapping_result is not None:
                scanner_pairs[i] = (j, [indexes for indexes in overlapping_result])
                break
    return scanner_pairs


def find_orientation(
        first_scanner: List[Tuple[int, int, int]],
        second_scanner: List[Tuple[int, int, int]],
        first_pair: Tuple[int, int],
        second_pair: Tuple[int, int],
) -> List[int]:
    for (i, direction) in enumerate(directions):
        first_first_position = rotate_position(first_scanner[first_pair[0]], direction)
        second_first_position = rotate_position(first_scanner[second_pair[0]], direction)
        first_distance = (
            second_scanner[first_pair[1]][0] - first_first_position[0],
            second_scanner[first_pair[1]][1] - first_first_position[1],
            second_scanner[first_pair[1]][2] - first_first_position[2],
        )
        second_distance = (
            second_scanner[second_pair[1]][0] - second_first_position[0],
            second_scanner[second_pair[1]][1] - second_first_position[1],
            second_scanner[second_pair[1]][2] - second_first_position[2],
        )
        if first_distance == second_distance:
            return direction


def set_points_to_origin(
        scanner_pairs: Dict[int, Tuple[int, List[Tuple[int, int]]]],
        scanners: List[List[Tuple[int, int, int]]],
        scanner_maps: List[List[List[int]]]
) -> Dict[int, Tuple[int, int, int]]:
    starting_points = {
        0: (0, 0, 0)
    }
    changed = True
    while changed:
        changed = False
        for from_mapping, (to_mapping, indexes) in scanner_pairs.items():
            if from_mapping in starting_points or to_mapping not in starting_points:
                continue
            changed = True
            direction = find_orientation(scanners[from_mapping], scanners[to_mapping], indexes[0], indexes[1])
            for i in range(len(scanners[from_mapping])):
                scanners[from_mapping][i] = rotate_position(scanners[from_mapping][i], direction)
            starting_points[from_mapping] = (
                starting_points[to_mapping][0] - (scanners[from_mapping][indexes[0][0]][0] - scanners[to_mapping][indexes[0][1]][0]),
                starting_points[to_mapping][1] - (scanners[from_mapping][indexes[0][0]][1] - scanners[to_mapping][indexes[0][1]][1]),
                starting_points[to_mapping][2] - (scanners[from_mapping][indexes[0][0]][2] - scanners[to_mapping][indexes[0][1]][2]),
            )
        if len(starting_points) != len(scanners):
            for i in range(len(scanners)):
                if i in starting_points:
                    continue
                for k in starting_points:
                    first_scanner_map = scanner_maps[i]
                    second_scanner_map = scanner_maps[k]
                    overlapping_result = find_overlapping(first_scanner_map, second_scanner_map, False)
                    if overlapping_result is not None:
                        scanner_pairs[i] = (k, [indexes for indexes in overlapping_result])
                        changed = True
                        break
    return starting_points


def parse_scanners() -> List[List[Tuple[int, int, int]]]:
    result = []
    current_scanner = None
    for line in sys.stdin:
        if line.strip() == "":
            continue
        if line.startswith("---"):
            current_scanner = []
            result.append(current_scanner)
            continue
        (x, y, z) = [int(c) for c in line.split(",")]
        current_scanner.append((x, y, z))
    return result


def solve():
    scanners = parse_scanners()
    scanner_maps = [build_distances_map(scanner) for scanner in scanners]
    print("DISTANCES BUILT")
    scanner_pairs = get_scanner_pairs(scanner_maps)
    print("PAIRS CALCULATED")
    starting_points = set_points_to_origin(scanner_pairs, scanners, scanner_maps)
    print("STARTING POINTS")
    points_from_zero = set(scanners[0])
    for i in range(1, len(scanners)):
        for (x, y, z) in scanners[i]:
            points_from_zero.add((x + starting_points[i][0], y + starting_points[i][1], z + starting_points[i][2]))

    return [p for p in points_from_zero if p[0] == -618], starting_points, len(points_from_zero)


if __name__ == '__main__':
    print(solve())
