"""Inverse complex delta field: z → X."""


def inverse_complex_delta_field(z) -> float:
    re = z.real if hasattr(z, 'real') else z[0]
    im = z.imag if hasattr(z, 'imag') else z[1]
    return 255.0 * re / (re + im) if (re + im) != 0 else 0.0