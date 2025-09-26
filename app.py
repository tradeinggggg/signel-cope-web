from flask import Flask, render_template, jsonify
from engine.signal_engine import SignalEngine
from notifier import Notifier
import json

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

signal_engine = SignalEngine(config["assets"])
notifier = Notifier(config["telegram_bot_token"], config["telegram_chat_id"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_signals", methods=["GET"])
def get_signals():
    results = []
    for asset in config["assets"]:
        signal = signal_engine.get_signal(asset)
        if signal:
            notifier.send_alert(asset, signal)
            results.append({
                "asset": asset,
                "signal": signal["signal"],
                "entry": round(signal["entry"], 4),
                "tp": round(signal["tp"], 4),
                "sl": round(signal["sl"], 4)
            })
        else:
            results.append({"asset": asset, "signal": "No signal"})
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
    application = app