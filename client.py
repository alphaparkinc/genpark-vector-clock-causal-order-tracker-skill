"""Vector Clock Causal Order Tracker.
100% Python Standard Library.
"""

import collections

class VectorClock:
    """Vector clock causality tracker for distributed event ordering."""
    def __init__(self, node_id, clock_dict=None):
        self.node_id = node_id
        self.clock = dict(clock_dict) if clock_dict else collections.defaultdict(int)

    def tick(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def merge(self, other_clock):
        for nid, val in other_clock.items():
            self.clock[nid] = max(self.clock.get(nid, 0), val)
        self.tick()

    def compare(self, other):
        all_keys = set(self.clock.keys()) | set(other.clock.keys())
        le = all(self.clock.get(k, 0) <= other.clock.get(k, 0) for k in all_keys)
        ge = all(self.clock.get(k, 0) >= other.clock.get(k, 0) for k in all_keys)

        if le and ge: return "EQUAL"
        if le: return "BEFORE"
        if ge: return "AFTER"
        return "CONCURRENT"
