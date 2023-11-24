from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline


class RandomForestModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):
        rf = make_pipeline(self.preprocessing, RandomForestRegressor(n_estimators=500, min_samples_split=5,
                                                                     min_samples_leaf=4, max_features=0.7, max_depth=10, bootstrap=False))
        rf.fit(X_train, y_train)
        self.model = rf

    def evaluate(self, X_test, y_test):
        print("RF MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("RF RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
