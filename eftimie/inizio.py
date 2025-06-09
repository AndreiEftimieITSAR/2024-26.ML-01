import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn import set_config

# Directory di output
output_dir = "eftimie/outputs"
os.makedirs(output_dir, exist_ok=True)

# Caricamento dati
df = pd.read_csv("eftimie/CarPrice_Assignment.csv")

X = df.drop(columns=['car_ID', 'CarName', 'price'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

results = {}

# Pipeline
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numerical_cols),
    ("cat", categorical_pipeline, categorical_cols)
])

# Random Forest base
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)
results["Random Forest Regressor"] = {
    "MAE": mean_absolute_error(y_test, y_pred),
    "MAPE": mean_absolute_percentage_error(y_test, y_pred)
}

# Linear Regression
model_lr = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])
model_lr.fit(X_train, y_train)
y_pred_lr = model_lr.predict(X_test)
results["Linear Regression"] = {
    "MAE": mean_absolute_error(y_test, y_pred_lr),
    "MAPE": mean_absolute_percentage_error(y_test, y_pred_lr)
}

# Grid Search RF
param_grid = {
    'regressor__n_estimators': [50, 100],
    'regressor__max_depth': [None, 10],
    'regressor__min_samples_split': [2, 5]
}
pipeline_rf = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])
grid_search = GridSearchCV(pipeline_rf, param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
y_pred_grid = best_model.predict(X_test)

results["Random Forest (Grid Search)"] = {
    "MAE": mean_absolute_error(y_test, y_pred_grid),
    "MAPE": mean_absolute_percentage_error(y_test, y_pred_grid)
}

# Confronto modelli
comparison_df = pd.DataFrame(results).T
comparison_df["MAE"] = comparison_df["MAE"].round(2)
comparison_df["MAPE (%)"] = (comparison_df["MAPE"] * 100).round(2)
comparison_df.drop(columns="MAPE", inplace=True)
comparison_df.to_csv(os.path.join(output_dir, "model_comparison.csv"))

# Parametri migliori
with open(os.path.join(output_dir, "best_params.txt"), "w") as f:
    f.write(str(grid_search.best_params_))

# Salvataggio modello
joblib.dump(best_model, os.path.join(output_dir, "best_model.pkl"))
print("Modello salvato in:", os.path.join(output_dir, "best_model.pkl"))
