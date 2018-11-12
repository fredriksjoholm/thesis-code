# coding=utf-8
import numpy as np
from sklearn import svm
import random
from scipy import sparse
from sklearn.base import BaseEstimator


class RESVM(BaseEstimator):
    """Implementation of robust ensemble SVMs"""

    def __init__(self, n_models=3, n_unl=1, n_pos=1, unl_penalty=1, rel_penalty=1, kernel='rbf'):
        """
        :type kernel: basestring
        """
        self.n_models = n_models
        self.n_unl = n_unl
        self.n_pos = n_pos
        self.unl_penalty = unl_penalty
        self.rel_penalty = rel_penalty
        self.kernel = kernel
        self.pos_penalty = unl_penalty * rel_penalty * n_unl / n_pos

        self.svms = None

    def fit(self, data, labels):
        self.svms = []
        pos_indices = [i for i, x in enumerate(labels) if x == 1]
        unl_indices = [i for i, x in enumerate(labels) if x == 0]

        for i in range(self.n_models):
            pos_sample_indices = random.sample(pos_indices, min(len(pos_indices), self.n_pos))
            unl_sample_indices = random.sample(unl_indices, min(len(unl_indices), int(self.n_unl*self.n_pos)))
            sample_indices = pos_sample_indices + unl_sample_indices
            if self.kernel == 'precomputed':
                samples = data[sample_indices][:, sample_indices]
            elif sparse.issparse(data):
                samples = data[sample_indices]
            else:
                samples = [data[i] for i in sample_indices]
            clf = svm.SVC(kernel=self.kernel,
                          class_weight={0: self.unl_penalty, 1: self.pos_penalty})
            target = [labels[i] for i in sample_indices]
            clf.fit(samples, target)
            self.svms.append((clf, sample_indices))

    def predict(self, data):
        if sparse.issparse(data):
            n_data = data.shape[0]
        else:
            n_data = len(data)
        result = np.zeros(n_data)
        for i in range(self.n_models):
            (clf, sample_indices) = self.svms[i]
            if self.kernel == 'precomputed':
                test_data = data[:, sample_indices]
            else:
                test_data = data
            classes = clf.predict(test_data)
            result += classes

        for (i, r) in enumerate(result[:]):
            if r > self.n_models / 2:
                result[i] = 1
            else:
                result[i] = 0
        return result

    def score(self, X, y):
        predict_result = self.predict(X)
        y_pos = [i for i in range(len(y)) if y[i] == 1]
        pred_pos = [i for i in range(len(y)) if predict_result[i] == 1]
        correct_pos = list(set(y_pos).intersection(pred_pos))

        if len(y_pos) == 0 or len(pred_pos) == 0 or len(correct_pos) == 0:
            return 0

        recall = len(correct_pos) / len(y_pos)
        py = len(pred_pos) / len(y)
        return (recall * recall) / py
