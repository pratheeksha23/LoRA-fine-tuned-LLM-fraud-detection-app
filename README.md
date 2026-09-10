# SentinelAI: FRAUD DETECTION APP

https://github.com/user-attachments/assets/f9e2e914-4395-404e-825c-c78dea8d82da

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

## Model Development & Distillation Architecture

### Phase 1: Parameter-Efficient Fine-Tuning (PEFT / LoRA)
* **Base Model:** Qwen/Qwen2.5-1.5B-Instruct
* **Fine-Tuning Method:** Low-Rank Adaptation (LoRA) via Hugging Face PEFT
* **Target Layers:** Query, key, value, and output projection layers (q_proj, k_proj, v_proj, o_proj)
* **Objective:** Train the model on complex financial telemetry to classify high-risk transactions while preventing false alarms on urgent late-night emergencies.
* **Artifacts:** Training scripts, configuration files, and evaluation workflows are maintained under the `/training` directory.

### Phase 2: High-Availability Edge Serving & Policy Distillation
* **Deployment Constraint:** Real-time payment processing requires sub-100ms response times and zero reliance on high-cost GPU infrastructure.
* **Distillation Approach:** The contextual decision boundaries and safety guardrails evaluated during LoRA fine-tuning were extracted into an ultra-low-latency rule-based inference engine.
* **Production Benefits:** Delivers instant risk scoring, zero external API token dependencies, and stable 100% uptime on CPU cloud environments.
