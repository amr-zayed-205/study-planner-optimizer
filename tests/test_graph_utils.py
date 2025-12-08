from src.models.chapter import Chapter
from src.algorithms.graph_utils import build_adjacency, detect_cycle, topological_sort, transitive_prereqs


def test_build_and_topo_no_cycle():
    chapters = [
        Chapter(id="A", title="A", time_minutes=10, score_value=1.0, prerequisites=[]),
        Chapter(id="B", title="B", time_minutes=20, score_value=2.0, prerequisites=["A"]),
        Chapter(id="C", title="C", time_minutes=30, score_value=3.0, prerequisites=["B"]),
    ]
    adj = build_adjacency(chapters)
    assert "A" in adj and "B" in adj and "C" in adj
    has_cycle, _ = detect_cycle(adj)
    assert not has_cycle
    topo = topological_sort(adj)
    assert topo and topo.index("A") < topo.index("B") < topo.index("C")
    tp = transitive_prereqs(adj)
    assert tp["C"] == {"A", "B"} or tp["C"] == {"B", "A"}


def test_cycle_detection():
    chapters = [
        Chapter(id="X", title="X", time_minutes=10, score_value=1.0, prerequisites=["Z"]),
        Chapter(id="Y", title="Y", time_minutes=20, score_value=2.0, prerequisites=["X"]),
        Chapter(id="Z", title="Z", time_minutes=30, score_value=3.0, prerequisites=["Y"]),
    ]
    adj = build_adjacency(chapters)
    has_cycle, cycle_nodes = detect_cycle(adj)
    assert has_cycle
    assert len(cycle_nodes) >= 2
