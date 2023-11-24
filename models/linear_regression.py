
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline


class LinearRegressionModel:
    def __init__(self, preprocessing):
        self.preprocessing = preprocessing
        self.model = None

    def train(self, X_train, y_train):
        lin_reg = make_pipeline(self.preprocessing, LinearRegression())
        lin_reg.fit(X_train, y_train)
        self.model = lin_reg

    def evaluate(self, X_test, y_test):
        print("Linear Regression MAE: ", mean_absolute_error(
            y_test, self.model.predict(X_test)))
        print("Linear Regression RMSE: ", mean_squared_error(
            y_test, self.model.predict(X_test), squared=False))
