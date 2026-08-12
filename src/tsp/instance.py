from dataclasses import dataclass
from typing import Optional


@dataclass
class TSPInstance:
    """
    Represents a symmetric Traveling Salesman Problem instance.
    """

    name: str
    dimension: int
    cost_matrix: list[list[float]]
    edge_weight_type: str
    coordinates: Optional[list[tuple[float, float]]] = None

    def distance(self, i: int, j: int) -> float:
        """Return the cost of traveling from city i to city j."""
        return self.cost_matrix[i][j]

    def is_symmetric(self) -> bool:
        """Check whether the cost matrix is symmetric."""
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.cost_matrix[i][j] != self.cost_matrix[j][i]:
                    return False

        return True