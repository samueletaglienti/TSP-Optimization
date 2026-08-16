from src.tsp.parser import load_tsplib


def test_load_gr17():
    instance = load_tsplib("data/tsplib/gr17.tsp")

    assert instance.name == "gr17"
    assert instance.dimension == 17
    assert instance.edge_weight_type == "EXPLICIT"

    assert instance.cost_matrix.shape == (17, 17)
    assert instance.is_symmetric()

    assert (instance.cost_matrix.diagonal() == 0).all()


def test_gr17_known_costs():
    instance = load_tsplib("data/tsplib/gr17.tsp")

    assert instance.cost_matrix[0, 1] == 633
    assert instance.cost_matrix[1, 0] == 633

    assert instance.cost_matrix[0, 2] == 257
    assert instance.cost_matrix[2, 0] == 257

    assert instance.cost_matrix[15, 16] == 336