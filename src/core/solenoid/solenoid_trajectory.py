"""Solenoid trajectory."""


def solenoid_trajectory(initial_value, n_steps=100):
    trajectory = []
    x = initial_value
    for i in range(n_steps):
        trajectory.append({"step": i, "value": x, "bit": int(x) & 1})
        x = (2 * x) % 1.0
    return trajectory