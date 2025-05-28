
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn import set_config
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

df = pd.read_csv("CarPrice_Assignment.csv")

df.head()

df.isnull().sum()

X = df.drop(columns=['car_ID', 'CarName', 'price'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

results = {}

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

model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

model_pipeline.fit(X_train, y_train)

y_pred = model_pipeline.predict(X_test)

results["Random Forest Regressor"] = {
    "MAE":  mean_absolute_error(y_test, y_pred),
    "MAPE": mean_absolute_percentage_error(y_test, y_pred)
}

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

param_grid = {
    'regressor__n_estimators': [50, 100, 200],
    'regressor__max_depth': [None, 10, 20],
    'regressor__min_samples_split': [2, 5]
}

pipeline_rf = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

grid_search = GridSearchCV(
    pipeline_rf,
    param_grid,
    cv=5,
    scoring='neg_mean_absolute_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print("Migliori parametri trovati con Grid Search:")
print(grid_search.best_params_)
print(f"\nMAE:  {mae:.2f}")
print(f"MAPE: {mape * 100:.2f}%")

results["Random Forest (Grid Search)"] = {
    "MAE": mae,
    "MAPE": mape
}

comparison_df = pd.DataFrame(results).T
comparison_df["MAE"] = comparison_df["MAE"].round(2)
comparison_df["MAPE (%)"] = (comparison_df["MAPE"] * 100).round(2)
comparison_df = comparison_df.drop(columns="MAPE")
print("\nConfronto modelli:\n")
print(comparison_df)

r2_lr = r2_score(y_test, y_pred_lr)  # Linear Regression
r2_rf = r2_score(y_test, model_pipeline.predict(X_test))  # Random Forest
r2_grid = r2_score(y_test, best_model.predict(X_test))  # Random Forest con GridSearch

print(f"R² Linear Regression:          {r2_lr:.4f}")
print(f"R² Random Forest:              {r2_rf:.4f}")
print(f"R² Random Forest (GridSearch): {r2_grid:.4f}")

set_config('pandas')

preprocessor_only = model_pipeline.named_steps['preprocessor']
X_test_transformed = preprocessor_only.transform(X_test)

num_columns = numerical_cols
cat_columns = preprocessor_only.named_transformers_['cat'].named_steps['encoder'].get_feature_names_out(categorical_cols)
all_columns = np.concatenate([num_columns, cat_columns])

X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=all_columns)
print("\nFeature trasformate (prime righe):\n")
print(X_test_transformed_df.head())

params = model_pipeline.get_params()
print("\nParametri del modello:\n")
print(params.keys())

import matplotlib.pyplot as plt
import seaborn as sns

# Distribuzione del target
sns.histplot(y, kde=True)
plt.title("Distribuzione dei prezzi delle auto")
plt.xlabel("Prezzo")
plt.show()

# Confronto tra valori reali e predetti
plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Prezzo reale")
plt.ylabel("Prezzo predetto")
plt.title("Predizioni vs Valori reali")
plt.grid(True)
plt.show()

importances = model_pipeline.named_steps["regressor"].feature_importances_
feature_names = all_columns
feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)

plt.figure(figsize=(10,6))
sns.barplot(x=feat_imp[:15], y=feat_imp.index[:15])
plt.title("Top 15 Feature Importance")
plt.ylabel("Feature")  
plt.xlabel("Importanza")
plt.tight_layout()
plt.show()