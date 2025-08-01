import sys
import os
from dataclasses import dataclass

from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import Custom_Exception
from src.logger import logging
from src.utils import save_object, eval_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Spliting Training and Test input data.")
            X_train, y_train , X_test, y_test = (train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1])

            models = {
                "Linear Regression" : LinearRegression(),
                "KNeighbors Regressor" : KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor" : RandomForestRegressor(),
                "XGBRegressor" : XGBRegressor(),
                "CatBoostRegressor" : CatBoostRegressor(verbose=False),
                "AdaBoostRegressor" : AdaBoostRegressor(),
                "GradientBoostingRegressor" : GradientBoostingRegressor()
            }

            params = {
    "Decision Tree": {
        'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
    },
    "Random Forest Regressor": {
        'n_estimators': [8, 16, 32, 64, 128, 256]
    },
    "GradientBoostingRegressor": {
        'learning_rate': [0.1, 0.01, 0.05, 0.001],
        'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
        'n_estimators': [8, 16, 32, 64, 128, 256]
    },
    "Linear Regression": {},
    "KNeighbors Regressor": {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'ball_tree', 'kd_tree']
    },
    "XGBRegressor": {
        'learning_rate': [0.1, 0.01, 0.05, 0.001],
        'n_estimators': [8, 16, 32, 64, 128, 256]
    },
    "CatBoostRegressor": {
        'depth': [6, 8, 10],
        'learning_rate': [0.01, 0.05, 0.1],
        'iterations': [30, 50, 100]
    },
    "AdaBoostRegressor": {
        'learning_rate': [0.1, 0.01, 0.5, 0.001],
        'n_estimators': [8, 16, 32, 64, 128, 256]
    }
}


            model_report : dict = eval_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models, params= params)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.65:
                raise Custom_Exception("No Best Model found.",sys)
            
            logging.info("Found Best model for the training and test data.")

            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)

            predicted=best_model.predict(X_test)
            r2=r2_score(y_test,predicted)

            return (best_model_name,r2*100)

        except Exception as e:
            raise Custom_Exception(e,sys)
            