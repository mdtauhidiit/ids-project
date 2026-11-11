import re

class RuleBasedIDS:
    def __init__(self):
        self.suspicious_flags = {"S0", "RSTOS0", "SH"}

    def evaluate(self, packet: dict) -> dict:
        failed_logins = int(packet.get("failed_logins", 0))
        serror_rate = float(packet.get("serror_rate", 0.0))
        same_srv_rate = float(packet.get("same_srv_rate", 1.0))
        src_bytes = int(packet.get("src_bytes", 0))
        dst_bytes = int(packet.get("dst_bytes", 0))
        flag = str(packet.get("flag", "SF")).upper()
        payload = str(packet.get("payload", ""))

        reasons = []

        if failed_logins >= 3:
            reasons.append(f"Brute-force pattern: {failed_logins} failed login attempts.")
        if flag in self.suspicious_flags or serror_rate > 0.7:
            reasons.append(f"SYN Flood / DoS indicator: flag={flag}, serror_rate={serror_rate}.")
        if same_srv_rate < 0.1 and src_bytes == 0:
            reasons.append("Port scan probe: low service affinity with zero payload bytes.")
        if src_bytes > 5000000 and dst_bytes < 1000:
            reasons.append("Data exfiltration pattern: high outbound to inbound byte ratio.")

        signatures = [r"(?i)(\.\./)", r"(?i)(union\s+select)", r"(?i)(/bin/sh)", r"(?i)(<script>)"]
        for pattern in signatures:
            if re.search(pattern, payload):
                reasons.append(f"Malicious string payload matched: {pattern}")
                break

        is_attack = len(reasons) > 0
        return {
            "prediction": "Attack" if is_attack else "Normal",
            "anomaly_detected": is_attack,
            "confidence": 1.0 if is_attack else 0.99,
            "violations": reasons,
            "method": "Rule-Based Engine"
        }