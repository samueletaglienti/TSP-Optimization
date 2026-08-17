from typing import Iterable


def build_tour(
    selected_arcs: Iterable[tuple[int, int]],
    start: int = 0,
) -> list[int]:
    """
    Reconstruct a TSP tour from selected directed arcs.

    The returned tour starts and ends at `start`.
    """

    successor = dict(selected_arcs)

    tour = [start]
    current = start

    while True:
        if current not in successor:
            raise ValueError(
                f"City {current} has no selected outgoing arc."
            )

        current = successor[current]
        tour.append(current)

        if current == start:
            break

        if len(tour) > len(successor) + 1:
            raise ValueError("The selected arcs contain a subtour.")

    return tour

def validate_tour(
    tour: list[int],
    n: int,
) -> None:
    """
    Validate that a tour is a Hamiltonian cycle on n cities.
    """

    if len(tour) != n + 1:
        raise ValueError(
            f"Invalid tour length: expected {n + 1}, got {len(tour)}."
        )

    if tour[0] != tour[-1]:
        raise ValueError("The tour does not return to the starting city.")

    visited = tour[:-1]

    if len(set(visited)) != n:
        raise ValueError("A city is visited more than once.")

    if set(visited) != set(range(n)):
        raise ValueError("The tour does not visit every city.")

def tour_cost(
    tour: list[int],
    cost_matrix,
) -> float:
    """
    Compute the total cost of a TSP tour.
    """

    return sum(
        cost_matrix[tour[k], tour[k + 1]]
        for k in range(len(tour) - 1)
    )