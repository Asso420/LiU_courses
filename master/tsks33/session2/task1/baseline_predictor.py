#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Optional, Tuple, List

import numpy as np
from matplotlib import pyplot as plt
from scipy.sparse.linalg import lsqr

from load_data import load_data, getA, nr_users, nr_movies, filename

@dataclass
class BaselineModel:

    def train_baseline(training_data):

        A = getA(training_data)
        r_bar = np.mean(training_data[:,2].astype(float))

        C = training_data[:,2].astype(float) - r_bar
        B = lsqr(A, C)[0]
        bu = B[:nr_users]
        bm = B[nr_users:] 

        return r_bar, bu, bm

    def predict(training_data, test_data):

        r_bar, bu, bm = BaselineModel.train_baseline(training_data)

        predictions = []
        for entry in test_data:
            u = entry[0]
            m = entry[1]
            pred = r_bar + bu[u] + bm[m]
            pred = max(1, min(5, pred))
            predictions.append(pred)

        return np.array(predictions)

    def rmse(predictions, test_data):

        actuals = test_data[:,2].astype(float)
        rmse = float(np.sqrt(np.mean((predictions - actuals)**2)))
        return rmse

    def abs_error_histogram(predictions, test_data, title):

        actuals = test_data[:, 2].astype(float)
        print("Predictions:", predictions)
        print("Actuals:", actuals)
        
        rounded_preds = np.rint(predictions)          # round to nearest integer
        rounded_preds = np.clip(rounded_preds, 1, 5)  # just in case

        print("Rounded Predictions:", rounded_preds)

        # absolute errors
        abs_errors = np.abs(rounded_preds - actuals)
        print("Absolute Errors:", abs_errors)

        plt.hist(
            abs_errors,
            bins=np.arange(-0.5, 5.5, 1), 
        )
        plt.xticks(range(0, 5))
        plt.title(title)
        plt.xlabel("Absolute error |rounded_pred - true|")
        plt.ylabel("Frequency")
        plt.show()


def main():
    
    training_data = load_data(filename + ".training")
    test_data = load_data(filename + ".test")

    # print("Training data:", training_data)
    # print("Test data:", test_data)

    train_pred = BaselineModel.predict(training_data, training_data)
    test_pred = BaselineModel.predict(training_data, test_data)

    train_rmse = BaselineModel.rmse(train_pred, training_data)
    test_rmse = BaselineModel.rmse(test_pred, test_data)

    print("Training predictions:", train_pred)
    print("Test predictions:", test_pred)
    print(f"Training RMSE: {train_rmse:.3f}")
    print(f"Test RMSE: {test_rmse:.3f}")

    
    BaselineModel.abs_error_histogram(test_pred, test_data, "Absolute errors on test data")

if __name__ == "__main__":
    main()