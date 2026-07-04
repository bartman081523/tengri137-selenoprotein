"""Tiny scikit-learn-free kNN classifier for embedding-vector inference.

Stored as a sibling module so pickle can find the class at load time,
independent of the entry-point script.
"""
import numpy as np


class NumpyKNNClassifier:
    def __init__(self, n_neighbors: int = 5, metric: str = "cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self._X = None
        self._y = None
        self._classes = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        self._X = X / norms
        self._y = y
        self._classes = np.unique(y)
        return self

    def _sim(self, X):
        X = np.asarray(X, dtype=np.float32)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        Xn = X / norms
        return Xn @ self._X.T

    def predict(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        out = np.empty(sim.shape[0], dtype=self._y.dtype)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            top = counts.max()
            cand = vals[counts == top]
            out[i] = cand.min()
        return out

    def predict_proba(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        proba = np.zeros((sim.shape[0], len(self._classes)), dtype=np.float32)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            for v, c in zip(vals, counts):
                j = int(np.searchsorted(self._classes, v))
                proba[i, j] = c / k
        return proba

    @property
    def classes_(self):
        return self._classes
