import os
import urllib.request
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTIFACT_DIR = os.path.join(BASE_DIR, "detection", "artifacts")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

TRAIN_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt"
TEST_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt"
TRAIN_FILE = os.path.join(DATA_DIR, "KDDTrain+.txt")
TEST_FILE = os.path.join(DATA_DIR, "KDDTest+.txt")

COLUMN_NAMES = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

FEATURE_COLS = ["duration", "src_bytes", "dst_bytes", "num_failed_logins", "same_srv_rate", "serror_rate"]

def download_data():
    for name, url, path in [("Train", TRAIN_URL, TRAIN_FILE), ("Test", TEST_URL, TEST_FILE)]:
        if not os.path.exists(path):
            print(f"Downloading {name} dataset...")
            urllib.request.urlretrieve(url, path)

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

def run():
    download_data()
    train_df = pd.read_csv(TRAIN_FILE, names=COLUMN_NAMES)
    test_df = pd.read_csv(TEST_FILE, names=COLUMN_NAMES)

    y_train = (train_df["label"] != "normal").astype(int).values
    y_test = (test_df["label"] != "normal").astype(int).values

    X_train_raw = train_df[FEATURE_COLS].astype(float).values
    X_test_raw = test_df[FEATURE_COLS].astype(float).values

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_preds) * 100:.2f}% | F1: {f1_score(y_test, rf_preds):.4f}")

    joblib.dump(rf, os.path.join(ARTIFACT_DIR, "ml_model.pkl"))
    joblib.dump(scaler, os.path.join(ARTIFACT_DIR, "ml_scaler.pkl"))

    print("Training PyTorch Neural Network...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader = DataLoader(
        TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)),
        batch_size=256,
        shuffle=True
    )

    model = IDSDeepNeuralNetwork(input_dim=len(FEATURE_COLS)).to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)

    model.train()
    for epoch in range(1, 16):
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            loss = criterion(model(bx), by)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_in = torch.tensor(X_test, dtype=torch.float32).to(device)
        dl_preds = (model(test_in).cpu().numpy().flatten() >= 0.5).astype(int)
    print(f"Deep Learning Accuracy: {accuracy_score(y_test, dl_preds) * 100:.2f}% | F1: {f1_score(y_test, dl_preds):.4f}")

    torch.save(model.state_dict(), os.path.join(ARTIFACT_DIR, "dl_model.pth"))
    print("Training finished! Artifacts saved to detection/artifacts/.")

if __name__ == "__main__":
    run()