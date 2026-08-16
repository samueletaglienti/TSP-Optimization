from pathlib import Path

import numpy as np

from src.tsp.instance import TSPInstance


def load_tsplib(file_path: str | Path) -> TSPInstance:
    """
    Load a symmetric TSP instance from a TSPLIB file.
    """
    file_path = Path(file_path)

    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    name = None
    problem_type = None
    dimension = None
    edge_weight_type = None
    edge_weight_format = None

    in_edge_weight_section = False
    edge_weights = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line == "EDGE_WEIGHT_SECTION":
            in_edge_weight_section = True
            continue

        if line == "EOF":
            break

        if in_edge_weight_section:
            edge_weights.extend(map(int, line.split()))
            continue

        if ":" in line:
            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            if key == "NAME":
                name = value

            elif key == "TYPE":
                problem_type = value

            elif key == "DIMENSION":
                dimension = int(value)

            elif key == "EDGE_WEIGHT_TYPE":
                edge_weight_type = value

            elif key == "EDGE_WEIGHT_FORMAT":
                edge_weight_format = value

    if problem_type != "TSP":
        raise ValueError(f"Unsupported problem type: {problem_type}")

    if dimension is None:
        raise ValueError("DIMENSION is missing.")

    if edge_weight_type != "EXPLICIT":
        raise ValueError(
            f"Unsupported EDGE_WEIGHT_TYPE: {edge_weight_type}"
        )

    if edge_weight_format != "LOWER_DIAG_ROW":
        raise ValueError(
            f"Unsupported EDGE_WEIGHT_FORMAT: {edge_weight_format}"
        )

    expected_weights = dimension * (dimension + 1) // 2

    if len(edge_weights) != expected_weights:
        raise ValueError(
            f"Expected {expected_weights} edge weights, "
            f"but found {len(edge_weights)}"
        )

    cost_matrix = np.zeros(
        (dimension, dimension),
        dtype=np.int64,
    )

    index = 0

    for i in range(dimension):
        for j in range(i + 1):
            cost = edge_weights[index]

            cost_matrix[i, j] = cost
            cost_matrix[j, i] = cost

            index += 1

    if not np.array_equal(cost_matrix, cost_matrix.T):
        raise ValueError("The cost matrix is not symmetric.")

    if not np.all(np.diag(cost_matrix) == 0):
        raise ValueError("The diagonal of the cost matrix must be zero.")

    return TSPInstance(
        name=name,
        dimension=dimension,
        edge_weight_type=edge_weight_type,
        cost_matrix=cost_matrix,
    )