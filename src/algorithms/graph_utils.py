from collections import defaultdict, deque
from typing import Dict, List, Tuple


def build_adjacency(chapters) -> Dict[str, List[str]]:
    """
    Build adjacency list (pre -> chapter).
    Example:
        If C2 depends on C1, then adjacency["C1"] = ["C2"]
    """
    adj = defaultdict(list)
    all_ids = {ch.id for ch in chapters}

    for ch in chapters:
        for pre in ch.prerequisites:
            adj[pre].append(ch.id)

        # تأكد إن كل شابتر موجود كمفتاح حتى لو ملوش مخارج
        if ch.id not in adj:
            adj[ch.id] = []

    return dict(adj)


def detect_cycle(adj: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    """
    Detect a directed cycle using DFS 3-color method.
    Returns (has_cycle, cycle_nodes) where cycle_nodes is a reconstructed cycle if found.
    If no cycle, returns (False, []).
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[str, int] = {u: WHITE for u in adj}
    parent: Dict[str, str] = {}
    cycle: List[str] = []

    def dfs(u: str) -> bool:
        nonlocal cycle
        color[u] = GRAY
        for v in adj.get(u, []):
            if color.get(v, WHITE) == WHITE:
                parent[v] = u
                if dfs(v):
                    return True
            elif color.get(v) == GRAY:
                # reconstruct cycle from u back to v
                path = [v]
                cur = u
                while cur != v and cur in parent:
                    path.append(cur)
                    cur = parent[cur]
                path.append(v)
                cycle = list(reversed(path))
                return True
        color[u] = BLACK
        return False

    for node in list(adj.keys()):
        if color[node] == WHITE:
            if dfs(node):
                return True, cycle
    return False, []



def topological_sort(adj: Dict[str, List[str]]) -> List[str]:
    """
    Kahn's algorithm.
    Return a valid topological order if the graph is a DAG.
    Return empty list if a cycle exists.
    """
    indegree = {node: 0 for node in adj}

    # احسب indegree لكل عقدة
    for u in adj:
        for v in adj[u]:
            indegree[v] += 1

    queue = deque([node for node in adj if indegree[node] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    # لو مفيش كل العقد تم ترتيبها → الجراف مش DAG
    if len(order) != len(adj):
        return []

    return order


def transitive_prereqs(adj: Dict[str, List[str]]) -> Dict[str, set]:
    """
    Compute all indirect + direct prerequisites for each node.
    Example:
        C3 -> needs C2
        C2 -> needs C1
        => C3 needs {C1, C2}
    """
    # reverse graph: chapter -> prerequisites
    rev = {node: [] for node in adj}

    for pre in adj:
        for ch in adj[pre]:
            rev[ch].append(pre)

    result = {}
    for node in rev:
        seen = set()
        stack = list(rev[node])

        while stack:
            p = stack.pop()
            if p not in seen:
                seen.add(p)
                stack.extend(rev[p])

        result[node] = seen

    return result
