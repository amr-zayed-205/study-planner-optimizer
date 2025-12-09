# 🌟 Study Planner Optimizer

A study-optimization system that selects the best chapters to study based on:

- ⏱ available time
- 📚 prerequisites
- ⭐ importance/value

using Graph Algorithms + Dynamic Programming + Exact 2ⁿ Search.

---

## Overview

Before exams, students often have many chapters but limited time. Each chapter has:

- **Study time** (minutes)
- **Score value** (importance)
- **Prerequisites** (required chapters)

**Goal:** choose the optimal subset of chapters that:

- ✔ fits within the available study time
- ✔ respects all prerequisite relationships
- ✔ gives the maximum total value

This system performs the full optimization automatically.

---

## 🔍 Algorithms Used

1. **Directed Graph Construction (Adjacency List)**

   - Represents each prerequisite as a directed edge: `A → B` (A must be studied before B).

2. **Cycle Detection (DFS – 3 Color Method)**

   - Detects invalid prerequisite loops (e.g., C1 → C2 → C1). If a cycle exists → planning becomes impossible.

3. **Topological Sort (Kahn’s Algorithm)**

   - Produces a valid study order that respects all prerequisites.

4. **Transitive Prerequisite Expansion**

   - Finds all required chapters (direct + indirect) for any node.

5. **Exact Subset Enumeration (2ⁿ) Optimization**

   - Because chapter count ≤ 20–22, the optimal solution is computed by evaluating all valid subsets and choosing the best one under the time limit.

---

## ✅ Requirements & Installation

All project dependencies are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

** Use the libirary **

- black
- pytest
- mypy
- ruff

> Note: The core algorithm uses standard Python libraries only; the listed packages are for development (formatting, linting, testing).

---

## 📁 Project Structure

```
project/
├── examples/
│   └── chapters_example.json
├── requirements.txt
├── src/
│   ├── ingestion/
│   │   └── reader.py
│   ├── algorithms/
│   │   ├── graph_utils.py
│   │   └── subset_optimizer.py
│   └── main.py
└── tests/
    └── test_*.py
```

---

## 🧾 Input Format (JSON)

The system loads chapters from a JSON file. Example entry:

```json
[
  {
    "id": "C1",
    "title": "Basics",
    "time_minutes": 120,
    "score_value": 10,
    "prerequisites": []
  },
  {
    "id": "C2",
    "title": "Data Structures",
    "time_minutes": 180,
    "score_value": 15,
    "prerequisites": ["C1"]
  }
]
```
---

## 🖼 Example Output

```
=== Optimal Study Plan ===
Best Value: 20.0
Best Time: 300

Chosen Chapters:
- C1 (Basics) — 120 minutes
- C2 (Data Structures) — 180 minutes
```

This result means:

- ✔ You can earn **20 points**
- ✔ Using exactly **300 minutes**
- ✔ By studying chapters `C1 → C2` in a valid order

---

## ▶️ How to Run

From the project root directory:

Run the main module:

```bash
py -m src.main
```

This will:

- Load the chapters JSON
- Build the graph
- Check for cycles
- Compute a valid order
- Run the exact optimizer
- Print the final optimal plan

Optional (run inside Python):

```py
from src.ingestion.reader import read_chapters_json
from src.algorithms.graph_utils import build_adjacency
from src.algorithms.subset_optimizer import exact_subset_search

chapters = read_chapters_json("examples/chapters_example.json")
adj = build_adjacency(chapters)
best_value, best_time, chosen = exact_subset_search(chapters, time_limit=300, adjacency_outgoing=adj)

for c in chosen:
    print(c)
```

---

## 🔬 Running Tests

The project includes unit tests for graph logic and the optimizer. Run them with:

```bash
py -m pytest -q
```


---

## 🚀 Future Improvements

- Command-Line Interface (`study-planner --file ... --time ...`)
- Visualization of the prerequisite graph (DAG)
- Streamlit dashboard for interactive planning
- FastAPI backend for web integration
- ML-based difficulty estimation for each chapter
- Saving study profiles for different students

---

## 🧑‍💻 Author

**Amr — AI & Backend Developer**

Building systems that combine algorithms, optimization, clean architecture, and real-world applications.

---

## 📌 Summary

This project demonstrates:

- Strong understanding of Graph Theory
- Strong understanding of Optimization & Dynamic Programming
- Clean modular code
- Realistic problem solving
- Professional project structure
- Fully tested components
- Ready for GitHub & graduation project

---


