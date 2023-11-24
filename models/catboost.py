from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from skopt import BayesSearchCV


class CatBoostModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):
        catboost = CatBoostRegressor(verbose=False)

        param_space = {
            'learning_rate': (0.01, 0.3, 'log-uniform'),
            'depth': (3, 10),
            'n_estimators': (100, 1000),
            'l2_leaf_reg': (1, 10),
            'subsample': (0.5, 1.0, 'uniform'),
            'colsample_bylevel': (0.5, 1.0, 'uniform'),
            'min_child_samples': (1, 20),
            'border_count': (1, 255)
        }

        cat_b = make_pipeline(self.preprocessing, BayesSearchCV(
            catboost, param_space, n_iter=5, scoring='neg_mean_squared_error', cv=5, verbose=False))

        cat_b.fit(X_train, y_train)
        self.model = cat_b

    def evaluate(self, X_test, y_test):
        print("Catboost MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("Catboost RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
