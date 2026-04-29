"""Encode data pattern as solenoid trajectory."""
from .encode_solenoid_trajectory import encode_solenoid_trajectory

def solenoid_encode_pattern(values, depth: int = 30):
    avg = sum(values) / len(values) if values else 0.0
    return encode_solenoid_trajectory(avg, depth)
