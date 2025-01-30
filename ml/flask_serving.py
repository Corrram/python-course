from flask import Flask, request, jsonify
import numpy as np
from keras.src.saving import load_model

app = Flask(__name__)
model = load_model("my_keras_model.h5")

@app.route("/", methods=["GET"])
def home():
    return "Hello from Flask! Go to /predict with a POST to get predictions."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json  # e.g. {"input": [3, 1, 22.0, 7.25]}
    X = np.array(data["input"]).reshape(1, -1)
    pred = model.predict(X)  # Might return shape (1,1)

    if pred.shape[1] == 1:
        pred = float(pred[0][0])

    return jsonify({"prediction": pred})

if __name__ == "__main__":
    app.run()