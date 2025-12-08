from src.ingestion.reader import read_chapters_json
from src.algorithms.graph_utils import build_adjacency, detect_cycle, topological_sort
from src.algorithms.subset_optimizer import exact_subset_search

# py -m src.main
def main():
    # Load data
    chapters = read_chapters_json("examples/chapters_example2.json")

    # Build graph
    adj = build_adjacency(chapters)

    # Cycle detection
    has_cycle, cycle_nodes = detect_cycle(adj)
    if has_cycle:
        print("❌ Error: Graph contains a cycle:", cycle_nodes)
        return

    # Topological order
    topo = topological_sort(adj)
    print("Topological order:", topo)

    # Run optimizer
    best_value, best_time, chosen = exact_subset_search(
        chapters, time_limit=550, adjacency_outgoing=adj
    )

    print("\n=== Optimal Study Plan ===")
    print("Best Value:", best_value)
    print("Best Time:", best_time)
    print("Chosen Chapters:")
    for c in chosen:
        print(f"- {c.id} ({c.title}) — {c.time_minutes} minutes")


if __name__ == "__main__":
    main()
