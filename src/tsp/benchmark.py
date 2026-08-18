from pathlib import Path
import csv

from src.tsp.parser import load_tsplib
from src.tsp.models.mtz import solve_mtz
from src.tsp.solution import validate_tour, tour_cost


def run_benchmark(instance_paths):
    """
    Run the MTZ model on a collection of TSP instances
    and collect the main experimental metrics.
    """

    results = []

    for path in instance_paths:
        path = Path(path)

        print(f"\n=== Solving {path.name} ===")

        instance = load_tsplib(path)
        result = solve_mtz(instance)

        # Validate the tour independently from the solver.
        tour_valid = False
        calculated_cost = None

        if result["tour"] is not None:
            try:
                validate_tour(result["tour"], instance.dimension)

                calculated_cost = int(
                    tour_cost(
                        result["tour"],
                        instance.cost_matrix,
                )
)

                tour_valid = True

            except ValueError as error:
                print(f"Invalid tour: {error}")

        results.append({
            "instance": instance.name,
            "dimension": instance.dimension,
            "status": result["status"],
            "objective": result["objective"],
            "tour_cost": calculated_cost,
            "tour_valid": tour_valid,
            "time": result["time"],
            "memory_mb": result["peak_memory_mb"],
            "variables": result["num_variables"],
            "constraints": result["num_constraints"],
        })

    return results


def save_results_csv(results, output_path):
    """
    Save benchmark results to a CSV file.
    """

    output_path = Path(output_path)

    fieldnames = [
        "instance",
        "dimension",
        "status",
        "objective",
        "tour_cost",
        "tour_valid",
        "time",
        "memory_mb",
        "variables",
        "constraints",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_path}")