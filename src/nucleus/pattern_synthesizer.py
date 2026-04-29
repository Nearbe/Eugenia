#!/usr/bin/env python3
"""Pattern Synthesizer — Generative engine for Nucleus."""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
from dataclasses import dataclass
from typing import List, cast

from core.linear.linear_algebra import CoreVector
from core.foundations.dual_number import dual_number
from core.transcendental.ln import ln
from core.transcendental.transcendentals import _arctan_inverse, pi
from nucleus.deterministic_core import SemanticPattern


@dataclass
class SynthesisResult:
    """Результат синтеза паттерна."""

    pattern: SemanticPattern
    velocity_magnitude: float
    method: str


class PatternSynthesizer:
    """Синтезатор паттернов — генеративное ядро Nucleus."""

    def _atan2(self, y: float, x: float) -> float:
        """Implementation of atan2 using core transcendental functions."""
        if x > 0:
            return _arctan_inverse(x / y) if y != 0 else 0.0
        if x < 0:
            val = _arctan_inverse(x / y) if y != 0 else 0.0
            return val + (pi() if y >= 0 else -pi())
        if x == 0:
            return pi() / 2 if y > 0 else -pi() / 2 if y < 0 else 0.0
        return 0.0

    def _create_pattern(self, vector: CoreVector, velocity: float, method: str) -> SemanticPattern:
        """Вспомогательный метод для создания нового паттерна из дуального состояния."""
        vec_list = vector.tolist()
        y = vec_list[1] if len(vec_list) > 1 else 0.0
        x = vec_list[0] if vec_list else 0.0
        phase = self._atan2(y, x)

        # Capacity is derived from the energy of the new vector and its growth velocity
        energy = sum(float(v) * float(v) for v in vec_list)
        capacity = -energy * cast(float, ln(max(energy, 1.0e-10))) / cast(float, ln(2.0)) + velocity

        return SemanticPattern(
            vector=vector, singular=float(velocity), capacity=float(capacity), phase=float(phase)
        )

    def interpolate(
        self, p1: SemanticPattern, p2: SemanticPattern, weight: float = 0.5
    ) -> SynthesisResult:
        """Линейная интерполяция через дуальное сложение."""
        d1 = dual_number(p1.vector, p1.singular)
        d2 = dual_number(p2.vector, p2.singular)

        # (p1 * (1-w)) + (p2 * w)
        res_d = d1.scale(1.0 - weight).add(d2.scale(weight))

        new_vec = CoreVector(cast(list[float], res_d.form))
        new_velocity = float(cast(float, res_d.velocity))

        return SynthesisResult(
            pattern=self._create_pattern(new_vec, new_velocity, "interpolation"),
            velocity_magnitude=new_velocity,
            method="interpolation",
        )

    def blend(self, p1: SemanticPattern, p2: SemanticPattern) -> SynthesisResult:
        """Нелинейное смешивание через дуальное умножение."""
        d1 = dual_number(p1.vector, p1.singular)
        d2 = dual_number(p2.vector, p2.singular)

        res_d = d1.multiply(d2)

        new_vec = CoreVector(cast(list[float], res_d.form))
        new_velocity = float(cast(float, res_d.velocity))

        return SynthesisResult(
            pattern=self._create_pattern(new_vec, new_velocity, "blending"),
            velocity_magnitude=new_velocity,
            method="blending",
        )

    def evolve(self, p: CoreVector, velocity: float = 1.0, factor: float = 1.1) -> SynthesisResult:
        """Эволюционный рост через дуальное возведение в степень."""
        d = dual_number(p, velocity)
        res_d = d.power(factor)

        new_vec = CoreVector(cast(list[float], res_d.form))
        new_velocity = float(cast(float, res_d.velocity))

        return SynthesisResult(
            pattern=self._create_pattern(new_vec, new_velocity, "evolution"),
            velocity_magnitude=new_velocity,
            method="evolution",
        )

    def synthesize_from_set(
        self, patterns: List[CoreVector], velocities: List[float], method: str = "interpolation"
    ) -> SynthesisResult:
        """Синтез из набора паттернов."""
        if not patterns:
            raise ValueError("No patterns provided for synthesis")
        if len(patterns) == 1:
            return self.evolve(patterns[0], velocities[0])

        if method == "interpolation":
            total_weight = len(patterns)
            res_d = dual_number(patterns[0], velocities[0]).scale(1.0 / total_weight)
            for i in range(1, len(patterns)):
                res_d = res_d.add(dual_number(patterns[i], velocities[i]).scale(1.0 / total_weight))
            new_vec = CoreVector(cast(list[float], res_d.form))
            new_velocity = float(cast(float, res_d.velocity))
        elif method == "blending":
            res_d = dual_number(patterns[0], velocities[0])
            for i in range(1, len(patterns)):
                res_d = res_d.multiply(dual_number(patterns[i], velocities[i]))
            new_vec = CoreVector(cast(list[float], res_d.form))
            new_velocity = float(cast(float, res_d.velocity))
        else:
            raise ValueError(f"Unknown synthesis method: {method}")

        return SynthesisResult(
            pattern=self._create_pattern(new_vec, new_velocity, method),
            velocity_magnitude=new_velocity,
            method=method,
        )

    def synthesize_from_set(
        self, patterns: List[SemanticPattern], method: str = "interpolation"
    ) -> SynthesisResult:
        """Синтез из набора паттернов."""
        if not patterns:
            raise ValueError("No patterns provided for synthesis")
        if len(patterns) == 1:
            return self.evolve(patterns[0])

        if method == "interpolation":
            total_weight = len(patterns)
            res_d = dual_number(patterns[0].vector, patterns[0].singular).scale(1.0 / total_weight)
            for i in range(1, len(patterns)):
                res_d = res_d.add(
                    dual_number(patterns[i].vector, patterns[i].singular).scale(1.0 / total_weight)
                )
            new_vec = CoreVector(cast(list[float], res_d.form))
            new_velocity = float(cast(float, res_d.velocity))
        elif method == "blending":
            res_d = dual_number(patterns[0].vector, patterns[0].singular)
            for i in range(1, len(patterns)):
                res_d = res_d.multiply(dual_number(patterns[i].vector, patterns[i].singular))
            new_vec = CoreVector(cast(list[float], res_d.form))
            new_velocity = float(cast(float, res_d.velocity))
        else:
            raise ValueError(f"Unknown synthesis method: {method}")

        return SynthesisResult(
            pattern=self._create_pattern(new_vec, new_velocity, method),
            velocity_magnitude=new_velocity,
            method=method,
        )


if __name__ == "__main__":
    # Quick test
    from nucleus.deterministic_core import SemanticPattern
    from core.linear.linear_algebra import CoreVector

    p1 = SemanticPattern(CoreVector([1.0, 0.0]), 1.0, 1.0, 0.0)
    p2 = SemanticPattern(CoreVector([0.0, 1.0]), 1.0, 1.0, 1.57)

    synth = PatternSynthesizer()
    res = synth.interpolate(p1, p2, 0.5)
    print(f"Interpolated: {res.pattern.vector}")
    print(f"Velocity: {res.velocity_magnitude}")
