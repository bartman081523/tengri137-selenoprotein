"""Pickle-safe NumpyKNNClassifier, separate file for sys.modules registration."""
import numpy as np


class NumpyKNNClassifier:
    """Tiny scikit-learn-free kNN classifier using cosine similarity."""

    def __init__(self, n_neighbors: int = 5, metric: str = "cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self._X = None
        self._y = None
        self._classes = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y)
        # L2-normalize for cosine similarity
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        self._X = (X / norms).astype(np.float32)
        self._y = y.astype(np.int64)
        self._classes = np.unique(self._y)
        return self

    def predict(self, X):
        proba = self.predict_proba(X)
        return self._classes[np.argmax(proba, axis=1)]

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float32)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        Xn = (X / norms).astype(np.float32)
        sim = Xn @ self._X.T  # (n_query, n_ref)
        n = min(self.n_neighbors, self._X.shape[0])
        # Top-k indices per query
        idx = np.argpartition(-sim, kth=n - 1, axis=1)[:, :n]
        proba = np.zeros((Xn.shape[0], len(self._classes)), dtype=np.float32)
        for i, inds in enumerate(idx):
            for j in inds:
                cls = int(self._y[j])
                proba[i, np.searchsorted(self._classes, cls)] += sim[i, j]
        # Normalize to vote fraction
        row_sum = proba.sum(axis=1, keepdims=True)
        row_sum = np.where(row_sum == 0, 1.0, row_sum)
        return proba / row_sum
