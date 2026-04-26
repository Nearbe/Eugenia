"""Sweep results."""


class SweepResults:
    __slots__ = ("thresholds", "occupancy_rates", "jump_events", "jump_count")
    
    def __init__(self, thresholds, occupancy_rates, jump_events, jump_count):
        self.thresholds = thresholds
        self.occupancy_rates = occupancy_rates
        self.jump_events = jump_events
        self.jump_count = jump_count