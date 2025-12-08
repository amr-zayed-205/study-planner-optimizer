# tests/test_subset_optimizer.py
from src.models.chapter import Chapter
from src.algorithms.graph_utils import build_adjacency
from src.algorithms.subset_optimizer import exact_subset_search


def test_exact_search_basic():
    chapters = [
        Chapter(id="C1", title="Basics", time_minutes=120, score_value=8, prerequisites=[]),
        Chapter(id="C2", title="DS", time_minutes=180, score_value=12, prerequisites=["C1"]),
        Chapter(id="C5", title="Greedy", time_minutes=90, score_value=7, prerequisites=["C1"]),
    ]
    adj = build_adjacency(chapters)
    best_value, best_time, chosen = exact_subset_search(chapters, time_limit=300, adjacency_outgoing=adj)
    # options:
    # - C1 + C2 -> time 300, value 20
    # - C1 + C5 -> time 210, value 15
    assert best_value >= 15
    assert best_time <= 300
    assert isinstance(chosen, list)


def test_impossible_prereq():
    # chapter C2 requires X which is not in list => C2 cannot be selected
    chapters = [
        Chapter(id="C1", title="A", time_minutes=60, score_value=5, prerequisites=[]),
        Chapter(id="C2", title="B", time_minutes=60, score_value=10, prerequisites=["X"]),  # X missing
    ]
    adj = build_adjacency(chapters)
    best_value, best_time, chosen = exact_subset_search(chapters, time_limit=200, adjacency_outgoing=adj)
    # only C1 is selectable
    assert best_value >= 5
    assert all(c.id != "C2" for c in chosen)
