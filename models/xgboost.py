from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
from skopt import BayesSearchCV


class XGBoostModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):
        regressor = XGBRegressor()

        param_space = {
            'learning_rate': (0.01, 0.3, 'log-uniform'),
            'max_depth': (3, 10),
            'n_estimators': (100, 1000),
            'subsample': (0.5, 1.0, 'uniform'),
            'colsample_bytree': (0.5, 1.0, 'uniform'),
            'colsample_bylevel': (0.5, 1.0, 'uniform'),
            'reg_lambda': (0.0, 1.0, 'uniform'),
            'reg_alpha': (0.0, 1.0, 'uniform'),
            'min_child_weight': (1, 10)
        }

        xgb = make_pipeline(self.preprocessing, BayesSearchCV(
            regressor, param_space, n_iter=1, scoring='neg_mean_squared_error', cv=5, verbose=False))
        xgb.fit(X_train, y_train)
        self.model = xgb

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        print("XGBoost MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("XGBoost RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
