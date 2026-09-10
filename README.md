# SentinelAI: FRAUD DETECTION APP
https://github.com/user-attachments/assets/6741bc99-b565-4a00-903e-7527779bec96

SentinelAI is a lightweight, context-aware financial fraud risk intelligence engine designed to detect unauthorized account takeovers, credential compromise, and fraudulent money-diversion patterns in real time.

---
## Overview

Traditional rule-based fraud detection often triggers false alarms on valid high-stress scenarios (such as late-night emergency hospital transfers or routine bill payments). SentinelAI analyzes complete transaction telemetry—weighing transaction amount, channel velocity, recipient novelty, and device telemetry to distinguish legitimate edge cases from active fraud vectors.

### Key Risk Signals Monitored
* **Device Telemetry:** Hardware ID consistency, trusted device age (>6 months), and IP geofencing.
* **Authentication Integrity:** Recent password resets, unexpected OTP interception, and session hijacking indicators.
* **Beneficiary Analysis:** Newly created payees (<10 minutes old), unverified third-party QR routing, and rapid batch dispersal across multiple accounts.
* **Contextual Nuance:** Emergency medical payments, utility bills, and trusted peer-to-peer transfers are protected against false positives.

---

## Tech Stack

* **Frontend & Dashboard:** Streamlit
* **Language:** Python 3.10+
* **Deployment Platform:** Streamlit Community Cloud

---

## Project Structure

```text
fraud-detection-app/
├── app.py              # Main Streamlit application and risk decision engine
├── requirements.txt    # Application dependencies
└── README.md           # Documentation

