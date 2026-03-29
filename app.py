from flask import Flask,render_template,request
import joblib
import numpy as np

app=Flask(__name__)
model = joblib.load("model/ids_model.pkl")
model_columns = joblib.load("model/model_columns.pkl")
protocol_columns = [c for c in model_columns if c.startswith("protocol_type_")]
service_columns = [c for c in model_columns if c.startswith("service_")]
flag_columns = [c for c in model_columns if c.startswith("flag_")]
numeric_columns = [
c for c in model_columns
if c not in protocol_columns + service_columns + flag_columns
]
print("Total Features:", len(model_columns))
@app.route("/")
def home():

    return render_template(
        "index.html",
        numeric_columns=numeric_columns,
        protocol_columns=protocol_columns,
        service_columns=service_columns,
        flag_columns=flag_columns
    )
@app.route("/predict", methods=["POST"])
def predict():

    numeric_features = []

    for col in model_columns:
        value = float(request.form[col])
        numeric_features.append(value)

    features = np.array(numeric_features).reshape(1,-1)

    prediction = model.predict(features)

    if prediction[0] == 0:
        result = "Normal Traffic"
    else:
        result = "Intrusion Detected"

    return render_template(
        "result.html",
        prediction_text=result
    )
if __name__=="__main__":
    print(model.n_features_in_)
    print(len(model_columns))
    app.run(debug=True)