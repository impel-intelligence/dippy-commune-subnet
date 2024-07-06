from dataclasses import dataclass
from datetime import datetime
from typing import Dict
import math
from subnet.common.node_entry import NodeEntry

def time_penalty(timestamp1: datetime, timestamp2: datetime) -> float:
    """
    Calculate time penalty based on the absolute time difference between two timestamps.
    The penalty increases exponentially, reaching a maximum of 3% after 1 hour.

    Args:
    timestamp1 (datetime): The first timestamp
    timestamp2 (datetime): The second timestamp

    Returns:
    float: The calculated penalty as a fraction (0.03 = 3%)
    """
    # Calculate absolute time difference
    time_diff = abs(timestamp1 - timestamp2)
    minutes_diff = time_diff.total_seconds() / 60

    # Constants
    MAX_PENALTY = 0.03  # 3%
    TIME_TO_MAX_PENALTY = 60  # 60 minutes (1 hour)

    # Calculate the exponential curve
    # We use the formula: penalty = MAX_PENALTY * (1 - e^(-k * minutes_diff))
    # where k is calculated to reach MAX_PENALTY at TIME_TO_MAX_PENALTY
    k = -math.log(1 - 0.99) / TIME_TO_MAX_PENALTY  # 0.99 to reach 99% of max at 1 hour

    penalty = MAX_PENALTY * (1 - math.exp(-k * minutes_diff))
    return min(penalty, MAX_PENALTY)  # Ensure we never exceed MAX_PENALTY


def compute_scores(entries: Dict[int, NodeEntry]) -> Dict[int, float]:
    wins = {id: 0 for id in entries}
    total_comparisons = {id: 0 for id in entries}

    for contestant_id, contestant_entry in entries.items():
        for challenger_id, challenger_entry in entries.items():
            if contestant_id == challenger_id:
                continue

            total_comparisons[contestant_id] += 1

            # Determine which entry is newer
            newer, older = (
                (contestant_entry, challenger_entry)
                if contestant_entry.submission_time > challenger_entry.submission_time
                else (challenger_entry, contestant_entry)
            )
            newer_id, older_id = (
                (contestant_id, challenger_id)
                if contestant_entry.submission_time  > challenger_entry.submission_time
                else (challenger_id, contestant_id)
            )

            # Apply time penalty if applicable
            if newer.initial_score <= 0.96:
                penalty = time_penalty(newer.submission_time , older.submission_time )
                adjusted_score_newer = newer.initial_score * (1 - penalty)
            else:
                adjusted_score_newer = newer.initial_score

            # Compare scores and update wins
            if adjusted_score_newer > older.initial_score:
                wins[newer_id] += 1
            elif adjusted_score_newer < older.initial_score:
                wins[older_id] += 1
            else:
                # In case of a tie, the older entry wins
                wins[older_id] += 1

    # Calculate initial scores
    initial_scores = {id: wins[id] / total_comparisons[id] for id in entries}

    # Find the maximum score
    max_score = max(initial_scores.values())

    # Normalize scores so that the highest is 1
    final_scores = {id: score / max_score for id, score in initial_scores.items()}

    return final_scores

