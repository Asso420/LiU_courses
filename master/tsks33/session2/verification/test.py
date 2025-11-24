#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect_data.py — Explain & print your ratings data and the design matrix mapping.
"""

from __future__ import annotations
import argparse
from typing import Optional
import numpy as np

HAVE_LOAD_MOD = False
HAVE_SCIPY = False
nr_users: Optional[int] = None
nr_movies: Optional[int] = None

try:
    import scipy.sparse as sp
    HAVE_SCIPY = True
except Exception:
    sp = None
    HAVE_SCIPY = False

try:
    from load_data import load_data as ld_load_data, nr_users as LD_USERS, nr_movies as LD_MOVIES
    HAVE_LOAD_MOD = True
    nr_users = int(LD_USERS)
    nr_movies = int(LD_MOVIES)
except Exception:
    HAVE_LOAD_MOD = False


def load_data_np_only(name: str) -> np.ndarray:
    data = np.genfromtxt(name, delimiter=',', dtype=int)
    data[:, 0:2] -= 1
    return data


def safe_load(name: str) -> np.ndarray:
    if HAVE_LOAD_MOD:
        return ld_load_data(name)
    return load_data_np_only(name)


def describe_dataset(data: np.ndarray, title: str) -> None:
    print(f"\n=== {title} ===")
    print(f"shape: {data.shape}  (rows ≈ ratings; columns = [user, movie, rating])")
    users = data[:, 0]
    movies = data[:, 1]
    ratings = data[:, 2]
    print(f"rows (ratings): {len(data)}")
    print(f"unique users:   {len(np.unique(users))}  | min={users.min()}  max={users.max()}")
    print(f"unique movies:  {len(np.unique(movies))} | min={movies.min()} max={movies.max()}")
    print(f"ratings range:  min={ratings.min()}  max={ratings.max()}  dtype={ratings.dtype}")
    if nr_users is not None and nr_movies is not None and nr_users > 0 and nr_movies > 0:
        possible = nr_users * nr_movies
        density = len(data) / possible
        print(f"declared totals  n_users={nr_users}  n_movies={nr_movies}")
        print(f"matrix density   {len(data)}/{possible} ≈ {density:.6f}")


def print_head(data: np.ndarray, title: str, n: int = 10) -> None:
    n = min(n, len(data))
    print(f"\n--- First {n} rows of {title} (0-based indices) ---")
    print("user,movie,rating")
    for i in range(n):
        u, m, r = map(int, data[i])
        print(f"{u},{m},{r}")


def preview_design_arrays(data: np.ndarray, preview: int = 10) -> None:
    n = len(data)
    r = np.concatenate((np.arange(n, dtype=int), np.arange(n, dtype=int)))
    # If global nr_users is unknown, use a safe offset inferred from data
    offset = nr_users if nr_users is not None else (data[:,0].max() + 1)
    c = np.concatenate((data[:, 0], data[:, 1] + offset))
    d = np.ones((2 * n,), dtype=float)

    print("\n--- Design-matrix construction preview (COO triplets) ---")
    print(f"nr_ratings = {n}")
    print(f"len(r) = {len(r)}, len(c) = {len(c)}, len(d) = {len(d)}")
    k = min(preview, len(r))
    print(f"r[:{k}] = {r[:k]}")
    print(f"c[:{k}] = {c[:k]}")
    print(f"d[:{k}] = {d[:k]}")

    if HAVE_SCIPY and nr_users is not None and nr_movies is not None:
        A = sp.csr_matrix((d, (r, c)), shape=(n, nr_users + nr_movies))
        print(f"A shape: {A.shape}  nnz={A.nnz}  (each row has two 1s)")
    else:
        print("SciPy not available or nr_users/nr_movies unknown — skipping CSR build.")


def main():
    parser = argparse.ArgumentParser(description="Inspect and print dataset contents")
    parser.add_argument("--filename", type=str, default="verification")
    parser.add_argument("--head", type=int, default=10)
    args = parser.parse_args()

    training_file = args.filename + ".training"
    test_file = args.filename + ".test"

    try:
        training = safe_load(training_file)
        test = safe_load(test_file)
    except Exception as e:
        print("Failed to load dataset files.")
        print("Error:", e)
        return

    print_head(training, "training", args.head)
    print_head(test, "test", args.head)
    describe_dataset(training, "training (stats)")
    describe_dataset(test, "test (stats)")
    preview_design_arrays(training, preview=max(10, args.head))


if __name__ == "__main__":
    main()