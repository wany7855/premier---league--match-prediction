from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier  

def create_models():
    logistic_model = LogisticRegression(
        max_iter=500,
        class_weight="balanced"
    )

    random_forest_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    xgboost_model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )

    return logistic_model, random_forest_model, xgboost_model

def train_models(
    logistic_model,
    random_forest_model,
    xgboost_model,
    train_x,
    train_y,
    xgboost_train_y
):
    logistic_model.fit(train_x, train_y)
    random_forest_model.fit(train_x, train_y)
    xgboost_model.fit(train_x, xgboost_train_y)


    return logistic_model, random_forest_model, xgboost_model


