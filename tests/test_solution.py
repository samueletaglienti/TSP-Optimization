import pytest

from src.tsp.solution import build_tour, validate_tour


def test_build_tour():
    arcs = [
        (0, 3),
        (1, 4),
        (2, 10),
        (3, 12),
        (4, 8),
        (5, 16),
        (6, 7),
        (7, 5),
        (8, 11),
        (9, 1),
        (10, 9),
        (11, 15),
        (12, 6),
        (13, 14),
        (14, 2),
        (15, 0),
        (16, 13),
    ]

    tour = build_tour(arcs)

    assert tour == [
        0, 3, 12, 6, 7, 5, 16, 13, 14,
        2, 10, 9, 1, 4, 8, 11, 15, 0
    ]


def test_validate_valid_tour():
    tour = [
        0, 3, 12, 6, 7, 5, 16, 13, 14,
        2, 10, 9, 1, 4, 8, 11, 15, 0
    ]

    validate_tour(tour, 17)


def test_validate_duplicate_city():
    tour = [
        0, 1, 2, 3, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 14, 15, 0
    ]

    with pytest.raises(ValueError):
        validate_tour(tour, 17)


def test_validate_missing_city():
    tour = [
        0, 1, 2, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 14, 15, 0
    ]

    with pytest.raises(ValueError):
        validate_tour(tour, 17)