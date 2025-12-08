# src/algorithms/subset_optimizer.py
from typing import Dict, List, Tuple
from ..models.chapter import Chapter
from ..algorithms.graph_utils import transitive_prereqs, topological_sort
from ..logger import get_logger

logger = get_logger(__name__)


def exact_subset_search(
    chapters: List[Chapter], time_limit: int, adjacency_outgoing: Dict[str, List[str]]
) -> Tuple[float, int, List[Chapter]]:
    """
    Exact subset enumeration optimizer (2^n).

    Args:
        chapters: list of Chapter objects (length n).
        time_limit: available time in minutes.
        adjacency_outgoing: adjacency dict (prerequisite -> list of chapters).

    Returns:
        best_value: maximum total score_value (float).
        best_time: total time in minutes corresponding to best subset.
        chosen_chapters: list of chosen Chapter objects in topological order.

    Notes:
        - A chapter is selectable only if all its transitive prerequisites (direct+indirect)
          are also present in the selected subset.
        - If a chapter requires a prerequisite not present in the chapters list,
          that chapter is considered impossible to select.
    """
    n = len(chapters)
    if n == 0:
        return 0.0, 0, []

    # map ids <-> indices for bitmasking
    id_to_idx: Dict[str, int] = {chap.id: i for i, chap in enumerate(chapters)}
    idx_to_ch: Dict[int, Chapter] = {i: chap for i, chap in enumerate(chapters)}

    times = [chap.time_minutes for chap in chapters]
    values = [chap.score_value for chap in chapters]

    # compute transitive prerequisites sets (ids)
    prereq_sets: Dict[str, set] = transitive_prereqs(adjacency_outgoing)

    # convert prereq sets -> bitmasks (aligned to indices)
    prereq_masks: List[int] = [0] * n
    impossible = [False] * n  # True if a chapter requires a prereq not present in our list
    for i in range(n):
        node_id = chapters[i].id
        reqs = prereq_sets.get(node_id, set())
        mask = 0
        for rid in reqs:
            if rid in id_to_idx:
                mask |= 1 << id_to_idx[rid]
            else:
                # missing prerequisite not in our chapters list -> this chapter cannot be selected
                impossible[i] = True
                break
        prereq_masks[i] = mask

    best_value = -1.0
    best_time = 0
    best_mask = 0

    total_masks = 1 << n

    # enumerate all subsets
    for mask in range(total_masks):
        total_time = 0
        total_value = 0.0
        valid = True

        m = mask
        i = 0
        # iterate bits of mask; break early for speed
        while m:
            if m & 1:
                # chapter i selected
                if impossible[i]:
                    valid = False
                    break
                total_time += times[i]
                if total_time > time_limit:
                    valid = False
                    break
                total_value += values[i]
                # check prereq mask satisfied (all prereq bits must be set)
                req_mask = prereq_masks[i]
                if (req_mask & mask) != req_mask:
                    valid = False
                    break
            i += 1
            m >>= 1

        if not valid:
            continue

        # update best (tie-breaker: smaller total time)
        if (total_value > best_value) or (total_value == best_value and total_time < best_time):
            best_value = total_value
            best_time = total_time
            best_mask = mask

    # build chosen ids in topological order (so prerequisites precede dependents)
    chosen_ids = {chapters[i].id for i in range(n) if (best_mask >> i) & 1}
    topo = topological_sort(adjacency_outgoing)
    if not topo:
        # fallback: preserve input order
        final_ids = [chap.id for chap in chapters if chap.id in chosen_ids]
    else:
        final_ids = [cid for cid in topo if cid in chosen_ids]

    chosen_list = [chap for cid in final_ids for chap in chapters if chap.id == cid]

    logger.info(
        "Exact subset search finished: best_value=%.2f, best_time=%d, chosen_count=%d",
        best_value,
        best_time,
        len(chosen_list),
    )
    return best_value, best_time, chosen_list
