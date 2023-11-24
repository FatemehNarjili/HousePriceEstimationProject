from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from skopt import BayesSearchCV


class KNNModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):
        knnreg = KNeighborsRegressor()
        param_space = {
            'n_neighbors': (1, 10),
            'weights': ['uniform', 'distance'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'leaf_size': (10, 50),
            'p': (1, 2)
        }

        knn = make_pipeline(self.preprocessing, BayesSearchCV(
            knnreg, param_space, n_iter=1, scoring='neg_mean_squared_error', cv=5, verbose=False))

        knn.fit(X_train, y_train)
        self.model = knn

    def evaluate(self, X_test, y_test):
        print("KNN MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("KNN RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
