#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import snap

import numpy as np
import scipy.sparse as sp

t_total0 = time.perf_counter()
TPATH = "/courses/TSKS33/ht2025/data/"


Edgelist = np.genfromtxt(TPATH + 'amazon0302.txt', dtype=int)
if np.min(Edgelist) == 1:
    Edgelist -= 1
N = np.max(Edgelist) + 1

A_rows = np.concatenate((Edgelist[:,1], Edgelist[:,0]))
A_cols = np.concatenate((Edgelist[:,0], Edgelist[:,1]))

A_rows, A_cols = zip(*set(zip(A_rows, A_cols)))  # de-dup
A = sp.csr_array((np.ones(len(A_rows)), (A_rows, A_cols)), shape=(N, N))

t0 = time.perf_counter()
k = np.asarray(A.sum(axis=1)).ravel().astype(np.int64)


connected_triples = int(((k * (k - 1)) // 2).sum())

three_stars = int(((k*(k-1)*(k-2)) // 6).sum())

A2 = A @ A
triangles = int((A.multiply(A2)).sum() // 6)

t1 = time.perf_counter()
t_total1 = time.perf_counter()

print("runtime:", t1 - t0)
print("total (load+build+compute):", t_total1 - t_total0)

print("Triangles:", triangles)
print("Connected triples:", connected_triples)
print("Three-stars:", three_stars)


