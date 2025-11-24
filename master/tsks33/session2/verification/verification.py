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


#--------------------task1------------------------------
@dataclass
class BaselineModel:

    def train_baseline(training_data_task2):

        A = getA(training_data_task2)
        r_bar = np.mean(training_data_task2[:,2].astype(float))

        C = training_data_task2[:,2].astype(float) - r_bar
        B = lsqr(A, C)[0]
        bu = B[:nr_users]
        bm = B[nr_users:] 

        return r_bar, bu, bm

    def predict(training_data_task2, test_data_task2):

        r_bar, bu, bm = BaselineModel.train_baseline(training_data_task2)

        predictions = []
        for entry in test_data_task2:
            u = entry[0]
            m = entry[1]
            pred = r_bar + bu[u] + bm[m]
            pred = max(1, min(5, pred))
            predictions.append(pred)

        return np.array(predictions)

    def rmse(predictions, test_data_task2):

        actuals = test_data_task2[:,2].astype(float)
        rmse = float(np.sqrt(np.mean((predictions - actuals)**2)))
        return rmse

    def abs_error_histogram(predictions, test_data_task2, title):

        actuals = test_data_task2[:, 2].astype(float)
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



#--------------------task2------------------------------

@dataclass
class neighborhoodModel:

    def build_residual_matrix(training_data_task2, r_bar, bu, bm):

        nr_ratings = len(training_data_task2)
        #r_bar,bu,bm = BaselineModel.train_baseline(training_data_task2)

        R = np.zeros((nr_users, nr_movies), dtype=float)
        rated = np.zeros((nr_users, nr_movies), dtype=bool)

        for u, m, r in training_data_task2:
            u = int(u); m = int(m); r = float(r)    
            baseline = r_bar + bu[u] + bm[m]
            baseline = clamp(baseline, 1, 5)

            R[u, m] = r - baseline
            rated[u, m] = True

        return R, rated

    def compute_cosine_similarity(R, rated, u_min=1):
        """
        Computes the cosine similarity matrix for the residuals.
        """
        sim = np.zeros((nr_movies, nr_movies), dtype=float)

        for i in range(nr_movies):
            sim[i, i] = 1.0
            for j in range(i + 1, nr_movies):
                common_users = rated[:, i] & rated[:, j]
                n_common = np.sum(common_users)
                if n_common >= u_min:
                    vec_i = R[common_users, i]
                    vec_j = R[common_users, j]

                    numerator = np.dot(vec_i, vec_j)
                    denominator = np.linalg.norm(vec_i) * np.linalg.norm(vec_j)
                    if denominator > 0:
                        s = numerator / denominator
                    else:
                        s = 0.0

                    sim[i, j] = s
                    sim[j, i] = s
        return sim

    # Verify D matrix for the verification dataset
    def verify_D_matrix(D, u_min):
        if filename == "verification" and u_min == 20:
            print("\nVerifying D matrix against verification_D_mat.npy...", D[0:5, 0:5])
            error_in_D = np.linalg.norm(np.load('verification_D_mat.npy') - D)
            print("Error in D matrix: {0:.5f}\n".format(error_in_D))

    # Evaluate the performance of the improved predictor
    def evaluate_improved_predictor(training_data_task2, test_data_task2, u_min, L):

        r_bar,bu,bm = BaselineModel.train_baseline(training_data_task2)
        R, rated = neighborhoodModel.build_residual_matrix(training_data_task2, r_bar, bu, bm)
        D = neighborhoodModel.compute_cosine_similarity(R, rated, u_min)
        neighborhoodModel.verify_D_matrix(D, u_min)

        predictions = []
        for u, m, _ in test_data_task2:
            u = int(u); m = int(m)

            weighted_sum = 0.0
            sim_sum = 0.0
            top_L_indices = np.argsort(-np.abs(D[m]))[:L]

            for j in top_L_indices:
                d_mj = D[m, j]
                sim_sum += abs(d_mj)

                if rated[u, j] != 0:
                    weighted_sum += d_mj * R[u, j]

            baseline = r_bar + bu[u] + bm[m]
            #baseline = clamp(baseline, 1, 5)

            if sim_sum > 0:
                r_hat = baseline + (weighted_sum / sim_sum)
            else:
                r_hat = baseline

            r_hat = clamp(r_hat, 1, 5)
            predictions.append(r_hat)

        return np.array(predictions)

def clamp(n, minimum, maximum):
    return max(min(n, maximum), minimum)


def main():
    L = 100 
    u_min = 20

    training_data_task2 = load_data(filename + ".training")
    test_data_task2 = load_data(filename + ".test")

    # print("Training data:", training_data_task2)
    # print("Test data:", test_data_task2)

    train_pred = BaselineModel.predict(training_data_task2, training_data_task2)
    test_pred = BaselineModel.predict(training_data_task2, test_data_task2)

    train_rmse = BaselineModel.rmse(train_pred, training_data_task2)
    test_rmse = BaselineModel.rmse(test_pred, test_data_task2)

    print("Training predictions:", train_pred)
    print("Test predictions:", test_pred)
    print(f"Training RMSE: {train_rmse:.3f}")
    print(f"Test RMSE: {test_rmse:.3f}")


    # BaselineModel.abs_error_histogram(test_pred, test_data_task2, "Absolute errors on test data")

    #--------------------task2-----------------------------

    neighborhood_pred_train = neighborhoodModel.evaluate_improved_predictor(
        training_data_task2, training_data_task2, u_min, L
        )
    
    neighborhood_pred_test = neighborhoodModel.evaluate_improved_predictor(
        training_data_task2, test_data_task2, u_min, L
    )

    train_rmse_neighborhood = BaselineModel.rmse(neighborhood_pred_train, training_data_task2)
    test_rmse_neighborhood = BaselineModel.rmse(neighborhood_pred_test, test_data_task2)
    
    print("Neighborhood Model Training RMSE: {0:.3f}".format(train_rmse_neighborhood))
    print("Neighborhood Model Test RMSE: {0:.3f}".format(test_rmse_neighborhood))
    
    print("\nTraining Improvement: {0:.3f}%".format(
        (train_rmse - train_rmse_neighborhood) / train_rmse * 100))
    print("Test Improvement: {0:.3f}%".format(
        (test_rmse - test_rmse_neighborhood) / test_rmse * 100))


if __name__ == "__main__":
    main()