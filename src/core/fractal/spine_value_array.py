"""Array of spine values: [D^0(Id), ..., D^n(Id)]."""

def spine_value_array(max_n):
    from .constants import D_ID
    return [D_ID ** i for i in range(max_n + 1)]
