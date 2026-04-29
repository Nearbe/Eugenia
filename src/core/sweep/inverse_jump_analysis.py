"""Inverse jump analysis."""
def inverse_jump_analysis(jump_events, n_back=10):
    return [{"event": event, "trace": [event[0] / (2 ** k) for k in range(n_back)]} for event in jump_events]
