"""Graphs for targeting and self-modification.

The full project includes additional graph types, but those depend on optional
packages which are unnecessary for the unit tests.  Only the lightweight
targeting and self‑modification graphs are exported here to keep imports
dependency free.
"""

from .targeting import build_targeting_graph, TargetState
from .self_mod import build_self_mod_graph, SelfModState

__all__ = [
    "build_targeting_graph",
    "TargetState",
    "build_self_mod_graph",
    "SelfModState",
]
