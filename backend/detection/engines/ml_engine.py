import os
import joblib
import numpy as np

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "../artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "ml_model.pkl")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "ml_scaler.pkl")

class MachineLearningIDS:
    def __init__(self):
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise FileNotFoundError("ML artifacts missing. Run 'python train_models.py' first.")
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def evaluate(self, packet: dict) -> dict:
        raw_vector = np.array([[
            float(packet.get("duration", 0)),
            float(packet.get("src_bytes", 0)),
            float(packet.get("dst_bytes", 0)),
            float(packet.get("failed_logins", 0)),
            float(packet.get("same_srv_rate", 1.0)),
            float(packet.get("serror_rate", 0.0))
        ]])

        scaled_vector = self.scaler.transform(raw_vector)
        probabilities = self.model.predict_proba(scaled_vector)[0]
        attack_prob = float(probabilities[1])
        is_attack = attack_prob >= 0.5

        return {
            "prediction": "Attack" if is_attack else "Normal",
            "anomaly_detected": is_attack,
            "confidence": round(attack_prob if is_attack else (1.0 - attack_prob), 4),
            "attack_probability": round(attack_prob, 4),
            "method": "Machine Learning (Random Forest)"
        }