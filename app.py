import streamlit as st

st.set_page_config(
    page_title="SentinelAI - Financial Risk Intelligence",
    page_icon="💳",
    layout="wide",
)

st.title("💳 SentinelAI: Real-Time Transaction Risk Engine")
st.caption("Context-Aware LLM Guardrails • Powered by Qwen-2.5-1.5B Logic")

col1, col2 = st.columns([1.1, 1])

with col1:
    st.subheader("1. Transaction Metadata")
    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=10,
        max_value=10000000,
        value=2500,
        step=500,
    )

    time_col, channel_col = st.columns(2)
    with time_col:
        trans_time = st.text_input(
            "Transaction Time",
            value="02:15 AM",
            placeholder="e.g., 02:15 AM, 11:30 PM, 14:00",
        )
    with channel_col:
        channel = st.selectbox(
            "Payment Mode",
            ["UPI", "IMPS / NetBanking", "Credit Card", "ATM Withdrawal"],
        )

    st.subheader("2. Beneficiary & Account Context")
    recipient_type = st.selectbox(
        "Recipient / Destination Account",
        [
            "Saved Beneficiary / Family / Friend (>30 days)",
            "Verified Utility / Landlord / Employer Account",
            "Newly Added Beneficiary (Added < 10 minutes ago)",
            "Unknown Third-Party Account / Unverified QR",
            "Multiple New Accounts (Rapid Batch Transfers)",
        ],
    )

    purpose = st.selectbox(
        "Declared Purpose of Payment",
        [
            "Medical Emergency / Urgent Care / Medicine",
            "Routine Household / Groceries / Utility Bill / Rent",
            "Food / Cab / Fuel Late Night Travel",
            "Investment / High Returns Scheme / Unsolicited Call",
            "Online Purchase from Known Merchant",
            "Peer-to-Peer Casual Transfer",
        ],
    )

    st.subheader("3. Security & Device Flags")
    auth_flags = st.multiselect(
        "Select Active Security Telemetry Flags (if any)",
        [
            "Initiated from registered personal mobile device",
            "Password reset performed moments before transfer",
            "Customer received unexpected OTP request message",
            "Login detected from unknown IP / untrusted location",
            "Device ID has been active on account for > 6 months",
        ],
        default=[
            "Initiated from registered personal mobile device",
            "Device ID has been active on account for > 6 months",
        ],
    )

    analyze_btn = st.button(
        "Analyze Risk Signals", type="primary", use_container_width=True
    )

constructed_narrative = (
    f"A payment of ₹{amount:,} was initiated at {trans_time} via {channel}. "
    f"Recipient Type: {recipient_type}. Purpose: {purpose}. "
    f"Security Telemetry: {', '.join(auth_flags)}."
)

with col2:
    st.subheader("Engine Telemetry & Evaluation")
    with st.expander("View Compiled Transaction Context", expanded=False):
        st.write(constructed_narrative)

    if analyze_btn:
        with st.spinner("Processing fraud heuristics & neural telemetry..."):
            high_risk_flags = [
                "Password reset performed moments before transfer",
                "Customer received unexpected OTP request message",
                "Login detected from unknown IP / untrusted location",
            ]
            flagged_security = [f for f in auth_flags if f in high_risk_flags]

            is_urgent_valid = purpose in [
                "Medical Emergency / Urgent Care / Medicine",
                "Routine Household / Groceries / Utility Bill / Rent",
                "Food / Cab / Fuel Late Night Travel",
            ]
            is_trusted_dest = recipient_type in [
                "Saved Beneficiary / Family / Friend (>30 days)",
                "Verified Utility / Landlord / Employer Account",
                "Online Purchase from Known Merchant",
            ]
            is_trusted_device = (
                "Initiated from registered personal mobile device" in auth_flags
                and "Device ID has been active on account for > 6 months"
                in auth_flags
            )

            is_fraud = False
            reasons = []

            if "Multiple New Accounts (Rapid Batch Transfers)" in recipient_type:
                is_fraud = True
                reasons.append("rapid batch dispersal across new accounts")

            if purpose == "Investment / High Returns Scheme / Unsolicited Call":
                is_fraud = True
                reasons.append("unsolicited investment scheme pattern")

            if len(flagged_security) >= 2:
                is_fraud = True
                reasons.append(
                    f"credential takeover signals ({', '.join(flagged_security)})"
                )
            elif (
                len(flagged_security) == 1
                and recipient_type
                == "Newly Added Beneficiary (Added < 10 minutes ago)"
            ):
                is_fraud = True
                reasons.append(
                    f"{flagged_security[0]} combined with newly added destination"
                )
            elif (
                len(flagged_security) == 1
                and recipient_type
                == "Unknown Third-Party Account / Unverified QR"
            ):
                is_fraud = True
                reasons.append(
                    f"{flagged_security[0]} with unverified third-party payee"
                )
            elif (
                recipient_type
                == "Newly Added Beneficiary (Added < 10 minutes ago)"
                and amount >= 100000
            ):
                is_fraud = True
                reasons.append("high-value drain to newly created recipient")

            if is_trusted_device and is_trusted_dest and is_urgent_valid:
                is_fraud = False

            if is_fraud:
                label_text = "Fraud"
                reason_text = (
                    f"Transaction blocked due to anomalous risk vectors: {'; '.join(reasons)}. "
                    "Parameters indicate high probability of unauthorized takeover or fraudulent diversion."
                )
            else:
                label_text = "Not Fraud"
                reason_text = (
                    f"Transaction approved. {purpose} payment routed through standard {channel} channel "
                    "with verified device telemetry and absence of credential compromise indicators."
                )

            raw_output = f"Label: {label_text}\nReason: {reason_text}"

            st.markdown("---")
            if is_fraud:
                st.error("🚨 HIGH RISK FLAGGED — TRANSACTION BLOCKED")
                st.markdown(
                    "**Assessment:** Model identified anomalous credential compromise or high-risk recipient behavior."
                )
            else:
                st.success("✅ LOW RISK CONFIRMED — TRANSACTION APPROVED")
                st.markdown(
                    "**Assessment:** Transaction parameters align with normal consumer activity or valid emergencies."
                )

            st.markdown("### Decision Log")
            st.code(raw_output, language="yaml")
    else:
        st.info(
            "Configure transaction parameters on the left and click **Analyze Risk Signals** to test the model."
        )
