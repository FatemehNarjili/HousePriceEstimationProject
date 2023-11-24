from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline


class LightGBMModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):

        light = make_pipeline(self.preprocessing, LGBMRegressor(
            boosting_type='gbdt',
            num_leaves=10,
            learnnig_rate=0.05, n_estimators=100, verbose=-1))

        light.fit(X_train, y_train)
        self.model = light

    def evaluate(self, X_test, y_test):
        print("LightGBM MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("LightGBM RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
