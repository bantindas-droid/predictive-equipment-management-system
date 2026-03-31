# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

history_data = []
maintenance_log = []

def calculate_score(temp, vib, pres, curr):
    value = (temp * 0.25 + vib * 0.25 + pres * 0.25 + curr * 0.25) / 100
    return round(value, 2)

def get_risk_level(score):
    if score > 0.7:
        return "High Risk"
    elif score > 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"

def generate_root_cause(temp, vib, pres):
    if vib > temp and vib > pres:
        return "High Vibration", "Possible bearing damage"
    elif temp > vib and temp > pres:
        return "High Temperature", "Overheating issue"
    elif pres > temp:
        return "High Pressure", "Pipeline stress detected"
    else:
        return "High Current", "Electrical overload risk"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    temp = float(request.form["temperature"])
    vib = float(request.form["vibration"])
    pres = float(request.form["pressure"])
    curr = float(request.form["current"])

    score = calculate_score(temp, vib, pres, curr)
    risk = get_risk_level(score)

    failure_time = datetime.now() + timedelta(hours=random.randint(48, 72))

    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": temp,
        "vibration": vib,
        "pressure": pres,
        "current": curr,
        "risk": risk,
        "score": score
    }

    history_data.append(record)

    return jsonify({
        "risk": risk,
        "score": score,
        "failure": failure_time.strftime("%Y-%m-%d %H:%M")
    })

@app.route("/history")
def history():
    return jsonify(history_data)

@app.route("/schedule")
def schedule():
    tasks = []
    for item in history_data[-5:]:
        tasks.append({
            "time": item["time"],
            "priority": item["risk"],
            "task": "Check machine components"
        })
    return jsonify(tasks)

@app.route("/cost")
def cost():
    predicted_cost = 3000 + random.randint(0, 2000)
    breakdown_cost = 12000 + random.randint(0, 3000)
    saving = breakdown_cost - predicted_cost

    return jsonify({
        "predicted": predicted_cost,
        "breakdown": breakdown_cost,
        "saving": saving
    })

@app.route("/root")
def root():
    if not history_data:
        return jsonify({"cause": "No data", "detail": "No analysis yet"})

    last = history_data[-1]
    cause, detail = generate_root_cause(
        last["temperature"],
        last["vibration"],
        last["pressure"]
    )

    return jsonify({
        "cause": cause,
        "detail": detail
    })

if __name__ == "__main__":
    app.run(debug=True)