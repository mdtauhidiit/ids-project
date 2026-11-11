import os
import joblib
import numpy as np
import torch
import torch.nn as nn

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "../artifacts")
TORCH_MODEL_PATH = os.path.join(ARTIFACT_DIR, "dl_model.pth")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "ml_scaler.pkl")

class IDSDeepNeuralNetwork(nn.Module):
    def __init__(self, input_dim=6):
        super(IDSDeepNeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

class DeepLearningIDS:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = IDSDeepNeuralNetwork(input_dim=6).to(self.device)

        if not os.path.exists(TORCH_MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise FileNotFoundError("DL artifacts missing. Run 'python train_models.py' first.")

        self.model.load_state_dict(torch.load(TORCH_MODEL_PATH, map_location=self.device))
        self.scaler = joblib.load(SCALER_PATH)
        self.model.eval()

    def evaluate(self, packet: dict) -> dict:
        raw_vector = np.array([[
            float(packet.get("duration", 0)),
            float(packet.get("src_bytes", 0)),
            float(packet.get("dst_bytes", 0)),
            float(packet.get("failed_logins", 0)),
            float(packet.get("same_srv_rate", 1.0)),
            float(packet.get("serror_rate", 0.0))
        ]])

        scaled = self.scaler.transform(raw_vector).astype(np.float32)
        tensor_in = torch.from_numpy(scaled).to(self.device)

        with torch.no_grad():
            prob = self.model(tensor_in).item()

        is_attack = prob >= 0.5
        return {
            "prediction": "Attack" if is_attack else "Normal",
            "anomaly_detected": is_attack,
            "confidence": round(prob if is_attack else (1.0 - prob), 4),
            "attack_probability": round(prob, 4),
            "method": "Deep Learning (PyTorch MLP)"
        }