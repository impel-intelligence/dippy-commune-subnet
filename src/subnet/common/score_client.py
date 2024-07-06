from typing import Dict

from communex.module.client import ModuleClient
from communex.types import Ss58Address

from config import settings
from subnet.common.node_entry import NodeEntry
from subnet.common.scoring import compute_scores

class ScoreClient:
    def __init__(self):
        return


    def normalize_scores(self, entries: Dict[int, NodeEntry]) -> Dict[int, float]:
        return compute_scores(entries)

