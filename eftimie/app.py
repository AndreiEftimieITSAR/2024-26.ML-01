from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Carica modello (assumiamo salvato come best_model.pkl)
model = joblib.load("outputs/best_model.pkl")

@app.route('/infer', methods=['POST'])
def infer():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return jsonify({"prediction": float(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)