from fractions import Fraction
from typing import Any


def _multiply_polynomials(poly1: list[Any], poly2: list[Any]) -> list[Any]:
    result = [Fraction() for _ in range(len(poly1) + len(poly2) - 1)]
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] += poly1[i] * poly2[j]
    return result


def _add_polynomials(poly1: list[Any], poly2: list[Any]) -> list[Any]:
    result = [Fraction() for _ in range(max(len(poly1), len(poly2)))]
    for i in range(len(poly1)):
        result[i] += poly1[i]
    for i in range(len(poly2)):
        result[i] += poly2[i]
    return result


def polynomial_interpolation(coordinates: list[tuple[int, int]]) -> list[Fraction]:
    n = len(coordinates)
    x_values, y_values = zip(*coordinates)

    coefficients = [Fraction() for _ in range(n)]
    for i in range(n):
        term = [Fraction(y_values[i])]
        for j in range(n):
            if j != i:
                term = _multiply_polynomials(term, [-x_values[j], 1])

        divisor = 1
        for j in range(n):
            if j != i:
                divisor *= x_values[i] - x_values[j]

        term = [c / divisor for c in term]
        coefficients = _add_polynomials(coefficients, term)

    return coefficients
