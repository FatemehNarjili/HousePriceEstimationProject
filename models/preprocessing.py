import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline


class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, gamma=1.0, random_state=None, n_init=10):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state
        self.n_init = n_init

    def fit(self, X, y=None, sample_weight=None):
        self.kmeans_ = KMeans(
            self.n_clusters, random_state=self.random_state, n_init=self.n_init)
        self.kmeans_.fit(X, sample_weight=sample_weight)
        return self

    def transform(self, X):
        return rbf_kernel(X, self.kmeans_.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, names=None):
        return [f"Cluster {i} similarity" for i in range(self.n_clusters)]


class Preprocessing(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.preprocessing = None

    def preprocess_data(self, df_train):
        log_pipeline = make_pipeline(
            FunctionTransformer(np.log, feature_names_out="one-to-one"),
            StandardScaler())
        default_num_pipeline = make_pipeline(StandardScaler())
        cluster_simil = ClusterSimilarity(
            n_clusters=20, gamma=1., random_state=42)

        preprocessing = ColumnTransformer([
            ("heavy_tail(area,floor)", log_pipeline, ["real_estate_area"]),
            ("regular_scale", default_num_pipeline, [
                "real_estate_age", "total_rooms", 'floor']),
            ("geo", cluster_simil, ["latitude", "longitude"]),
        ])

        preprocessing.fit(df_train)
        self.preprocessing = preprocessing
        return self.preprocessing

    def transform(self, df):
        return self.preprocessing.transform(df)

    def get_feature_names_out(self):
        return self.preprocessing.get_feature_names_out()
