"""
Unit test untuk modul fuzzy/membership.py.
Menguji nilai di titik batas, puncak, dan di luar rentang
untuk fungsi keanggotaan segitiga dan trapesium.
"""

import pytest
import numpy as np
from app.fuzzy.membership import triangular_membership, trapezoidal_membership


def test_triangular_membership_scalar():
    """Menguji trimf pada titik batas, puncak, sisi miring, dan di luar rentang."""
    # Segitiga a=10, b=20, c=30
    a, b, c = 10.0, 20.0, 30.0

    # Di luar rentang kiri
    assert triangular_membership(5.0, a, b, c) == 0.0
    assert triangular_membership(10.0, a, b, c) == 0.0

    # Sisi miring kiri
    assert triangular_membership(15.0, a, b, c) == pytest.approx(0.5)

    # Titik puncak
    assert triangular_membership(20.0, a, b, c) == 1.0

    # Sisi miring kanan
    assert triangular_membership(25.0, a, b, c) == pytest.approx(0.5)

    # Di luar rentang kanan
    assert triangular_membership(30.0, a, b, c) == 0.0
    assert triangular_membership(35.0, a, b, c) == 0.0


def test_trapezoidal_membership_scalar():
    """Menguji trapmf pada titik batas, puncak datar, sisi miring, dan di luar rentang."""
    # Trapesium a=10, b=20, c=30, d=40
    a, b, c, d = 10.0, 20.0, 30.0, 40.0

    # Di luar rentang kiri
    assert trapezoidal_membership(5.0, a, b, c, d) == 0.0
    assert trapezoidal_membership(10.0, a, b, c, d) == 0.0

    # Sisi miring kiri
    assert trapezoidal_membership(15.0, a, b, c, d) == pytest.approx(0.5)

    # Puncak datar
    assert trapezoidal_membership(20.0, a, b, c, d) == 1.0
    assert trapezoidal_membership(25.0, a, b, c, d) == 1.0
    assert trapezoidal_membership(30.0, a, b, c, d) == 1.0

    # Sisi miring kanan
    assert trapezoidal_membership(35.0, a, b, c, d) == pytest.approx(0.5)

    # Di luar rentang kanan
    assert trapezoidal_membership(40.0, a, b, c, d) == 0.0
    assert trapezoidal_membership(45.0, a, b, c, d) == 0.0


def test_trapezoidal_edge_open_left_and_right():
    """Menguji trapesium bahu kiri terbuka (a=b) dan bahu kanan terbuka (c=d)."""
    # Bahu kiri terbuka: a=0, b=0, c=2, d=4
    assert trapezoidal_membership(-1.0, 0, 0, 2, 4) == 1.0
    assert trapezoidal_membership(0.0, 0, 0, 2, 4) == 1.0
    assert trapezoidal_membership(1.0, 0, 0, 2, 4) == 1.0
    assert trapezoidal_membership(3.0, 0, 0, 2, 4) == pytest.approx(0.5)
    assert trapezoidal_membership(4.0, 0, 0, 2, 4) == 0.0

    # Bahu kanan terbuka: a=6, b=8, c=10, d=10
    assert trapezoidal_membership(5.0, 6, 8, 10, 10) == 0.0
    assert trapezoidal_membership(7.0, 6, 8, 10, 10) == pytest.approx(0.5)
    assert trapezoidal_membership(8.0, 6, 8, 10, 10) == 1.0
    assert trapezoidal_membership(10.0, 6, 8, 10, 10) == 1.0
    assert trapezoidal_membership(12.0, 6, 8, 10, 10) == 1.0


def test_membership_numpy_array():
    """Menguji fungsi keanggotaan pada array NumPy."""
    x = np.array([0.0, 15.0, 20.0, 25.0, 50.0])
    mu_tri = triangular_membership(x, 10.0, 20.0, 30.0)
    expected_tri = np.array([0.0, 0.5, 1.0, 0.5, 0.0])
    np.testing.assert_allclose(mu_tri, expected_tri)

    mu_trap = trapezoidal_membership(x, 10.0, 20.0, 30.0, 40.0)
    expected_trap = np.array([0.0, 0.5, 1.0, 1.0, 0.0])
    np.testing.assert_allclose(mu_trap, expected_trap)


def test_invalid_parameters():
    """Memastikan exception dilempar jika parameter urutan salah (a > b atau b > c)."""
    with pytest.raises(ValueError):
        triangular_membership(10, 30, 20, 10)

    with pytest.raises(ValueError):
        trapezoidal_membership(10, 40, 30, 20, 10)
