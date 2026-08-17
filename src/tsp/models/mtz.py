import time

from highspy import Highs, HighsVarType

from src.tsp.instance import TSPInstance

from src.tsp.memory import PeakMemoryMonitor


def solve_mtz(instance: TSPInstance, time_limit: float = 120.0):
    """
    Solve a symmetric TSP instance using the MTZ formulation.

    Parameters
    ----------
    instance : TSPInstance
        TSP instance to solve.

    time_limit : float
        Maximum solving time in seconds.

    Returns
    -------
    dict
        Experimental results of the optimization.
    """

    highs = Highs()

    highs.setOptionValue("time_limit", time_limit)
    highs.setOptionValue("output_flag", False)

    n = instance.dimension

    # ---------------------------------------------------------
    # Decision variables x[i,j]
    # ---------------------------------------------------------

    x = {}

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            x[i, j] = highs.addVariable(
                lb=0,
                ub=1,
                type=HighsVarType.kInteger,
                name=f"x_{i}_{j}",
            )

    # ---------------------------------------------------------
    # Degree constraints
    # ---------------------------------------------------------

    # One outgoing arc from every city.
    for i in range(n):
        expression = sum(
            x[i, j]
            for j in range(n)
            if j != i
        )

        highs.addConstr(expression == 1)

    # One incoming arc to every city.
    for j in range(n):
        expression = sum(
            x[i, j]
            for i in range(n)
            if i != j
        )

        highs.addConstr(expression == 1)

    # ---------------------------------------------------------
    # Objective function
    # ---------------------------------------------------------

    objective = sum(
        instance.cost_matrix[i, j] * x[i, j]
        for i in range(n)
        for j in range(n)
        if i != j
    )

    highs.minimize(objective)

    # ---------------------------------------------------------
    # MTZ auxiliary variables
    # ---------------------------------------------------------

    u = {}

    for i in range(1, n):
        u[i] = highs.addVariable(
            lb=1,
            ub=n - 1,
            type=HighsVarType.kInteger,
            name=f"u_{i}",
        )

    # ---------------------------------------------------------
    # MTZ subtour elimination constraints
    # ---------------------------------------------------------

    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                continue

            highs.addConstr(
                u[i] - u[j] + n * x[i, j] <= n - 1
            )

    # ---------------------------------------------------------
    # Solve
    # ---------------------------------------------------------

    memory_monitor = PeakMemoryMonitor()

    memory_monitor.start()

    start_time = time.perf_counter()

    highs.run()

    elapsed_time = time.perf_counter() - start_time

    memory_monitor.stop()

    # ---------------------------------------------------------
    # Solver information
    # ---------------------------------------------------------

    info = highs.getInfo()

    model_status = highs.modelStatusToString(highs.getModelStatus())

    objective_value = info.objective_function_value
    mip_gap = info.mip_gap
    best_bound = info.mip_dual_bound

    # ---------------------------------------------------------
    # Extract selected arcs
    # ---------------------------------------------------------

    selected_arcs = []

    for (i, j), variable in x.items():

        value = highs.variableValue(variable)

        if value > 0.5:
            selected_arcs.append((i, j))

    # ---------------------------------------------------------
    # Reconstruct tour
    # ---------------------------------------------------------

    tour = []

    if selected_arcs:

        successor = {
            i: j
            for i, j in selected_arcs
        }

        current = 0
        tour.append(current)

        for _ in range(n):
            if current not in successor:
                break

            current = successor[current]
            tour.append(current)

    # ---------------------------------------------------------
    # Model size
    # ---------------------------------------------------------

    num_variables = highs.getNumCol()
    num_constraints = highs.getNumRow()

    # ---------------------------------------------------------
    # Return experimental results
    # ---------------------------------------------------------

    return {
        "model": "MTZ",
        "status": model_status,
        "objective": objective_value,
        "best_bound": best_bound,
        "gap": mip_gap,
        "time": elapsed_time,
        "peak_memory_mb": memory_monitor.peak_memory_mb,
        "tour": tour,
        "selected_arcs": selected_arcs,
        "num_variables": num_variables,
        "num_constraints": num_constraints,
    }