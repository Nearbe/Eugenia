"""Binary encoding of delta_value as solenoid trajectory."""


def encode_solenoid_trajectory(delta_value: float, depth: int = 30) -> list[int]:
    bits = []
    x = delta_value
    for _ in range(depth):
        bits.append(int(x) & 1)
        x = (2 * x) % 1.0
    return bits