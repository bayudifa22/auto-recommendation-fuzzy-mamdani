"""
Modul fungsi keanggotaan fuzzy (Fuzzy Membership Functions).
Mengimplementasikan fungsi keanggotaan segitiga (triangular) dan trapesium (trapezoidal)
secara manual menggunakan NumPy untuk perhitungan skalar maupun array.
"""

from typing import Union
import numpy as np


def triangular_membership(
    x: Union[float, int, np.ndarray],
    a: float,
    b: float,
    c: float
) -> Union[float, np.ndarray]:
    """
    Menghitung derajat keanggotaan fungsi segitiga (trimf).

    Parameter:
        x: Nilai input (skalar atau array NumPy)
        a: Titik kaki kiri segitiga (mu = 0)
        b: Titik puncak segitiga (mu = 1)
        c: Titik kaki kanan segitiga (mu = 0)

    Kondisi: a <= b <= c

    Return:
        Derajat keanggotaan dalam rentang [0.0, 1.0]
    """
    if a > b or b > c:
        raise ValueError(f"Parameter segitiga tidak valid: harus a <= b <= c (diterima: {a}, {b}, {c})")

    # Jika x adalah skalar float/int
    if np.isscalar(x):
        val = float(x)
        if val <= a or val >= c:
            return 0.0
        if val == b:
            return 1.0
        if a < val < b:
            return (val - a) / (b - a) if b > a else 1.0
        if b < val < c:
            return (c - val) / (c - b) if c > b else 1.0
        return 0.0

    # Jika x adalah array NumPy
    x_arr = np.asarray(x, dtype=float)
    mu = np.zeros_like(x_arr, dtype=float)

    # Wilayah naik: a < x <= b
    if b > a:
        left_mask = (x_arr > a) & (x_arr <= b)
        mu[left_mask] = (x_arr[left_mask] - a) / (b - a)
    elif a == b:
        mu[x_arr == b] = 1.0

    # Wilayah turun: b < x < c
    if c > b:
        right_mask = (x_arr > b) & (x_arr < c)
        mu[right_mask] = (c - x_arr[right_mask]) / (c - b)

    # Titik puncak pasti 1.0
    mu[x_arr == b] = 1.0

    return np.clip(mu, 0.0, 1.0)


def trapezoidal_membership(
    x: Union[float, int, np.ndarray],
    a: float,
    b: float,
    c: float,
    d: float
) -> Union[float, np.ndarray]:
    """
    Menghitung derajat keanggotaan fungsi trapesium (trapmf).

    Parameter:
        x: Nilai input (skalar atau array NumPy)
        a: Titik kaki kiri (mu mulai naik dari 0)
        b: Titik bahu kiri (mu mencapai 1)
        c: Titik bahu kanan (mu mulai turun dari 1)
        d: Titik kaki kanan (mu mencapai 0)

    Kondisi: a <= b <= c <= d

    Return:
        Derajat keanggotaan dalam rentang [0.0, 1.0]
    """
    if a > b or b > c or c > d:
        raise ValueError(f"Parameter trapesium tidak valid: harus a <= b <= c <= d (diterima: {a}, {b}, {c}, {d})")

    if np.isscalar(x):
        val = float(x)
        # Kasus tepi kiri terbuka (a == b)
        if a == b and val <= b:
            return 1.0
        # Kasus tepi kanan terbuka (c == d)
        if c == d and val >= c:
            return 1.0
        # Di luar jangkauan
        if val <= a or val >= d:
            return 0.0
        # Puncak datar
        if b <= val <= c:
            return 1.0
        # Sisi miring kiri
        if a < val < b:
            return (val - a) / (b - a) if b > a else 1.0
        # Sisi miring kanan
        if c < val < d:
            return (d - val) / (d - c) if d > c else 1.0
        return 0.0

    x_arr = np.asarray(x, dtype=float)
    mu = np.zeros_like(x_arr, dtype=float)

    # Tepi kiri terbuka
    if a == b:
        mu[x_arr <= b] = 1.0
    elif b > a:
        left_mask = (x_arr > a) & (x_arr < b)
        mu[left_mask] = (x_arr[left_mask] - a) / (b - a)

    # Puncak datar
    mu[(x_arr >= b) & (x_arr <= c)] = 1.0

    # Tepi kanan terbuka
    if c == d:
        mu[x_arr >= c] = 1.0
    elif d > c:
        right_mask = (x_arr > c) & (x_arr < d)
        mu[right_mask] = (d - x_arr[right_mask]) / (d - c)

    return np.clip(mu, 0.0, 1.0)
