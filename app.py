import streamlit as st
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

st.set_page_config(
    page_title="SentinelAI - Financial Risk Intelligence",
    page_icon="💳",
    layout="wide",
)

st.title("💳 SentinelAI: Real-Time Transaction Risk Engine")
st.caption("Context-Aware LLM Guardrails • Powered by Qwen-2.5-1.5B + LoRA Adapter")


@st.cache_resource
def load_model():
    base_model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    adapter_repo = "YOUR_HF_USERNAME/fraud-lora-adapter"

    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )

    model = PeftModel.from_pretrained(base_model, adapter_repo)
    model.eval()
    if hasattr(model, "gradient_checkpointing_disable"):
        model.gradient_checkpointing_disable()
    model.config.use_cache = True
    return tokenizer, model


tokenizer, model = load_model()

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
        with st.spinner("Processing fraud heuristics & neural weights..."):
            system_prompt = (
                "You are an expert fraud risk auditor for a premier bank. Analyze the complete context:\n"
                "- Emergency transfers, family support, groceries, utility bills, or small late-night spends on a trusted device are NOT FRAUD.\n"
                "- Only declare FRAUD if there are unmistakable fraud flags: unauthorized device logins, OTP interception, password resets followed by large drains, or rapid transfers to brand new beneficiaries.\n\n"
                "Respond strictly in this format:\n"
                "Label: <Fraud or Not Fraud>\n"
                "Reason: <concise 1-2 sentence breakdown>"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following financial transaction.\n\n"
                        f"Transaction: {constructed_narrative}\n\n"
                        "Determine whether it is Fraud or Not Fraud. Then provide a short reason.\n\n"
                        "Respond in exactly this format:\n"
                        "Label: <Fraud or Not Fraud>\n"
                        "Reason: <short explanation>"
                    ),
                },
            ]

            prompt_text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = tokenizer([prompt_text], return_tensors="pt").to(model.device)

            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=90, do_sample=False)

            raw_output = tokenizer.decode(
                outputs[0][inputs.input_ids.shape[1] :], skip_special_tokens=True
            ).strip()
            is_fraud = "label: fraud" in raw_output.lower() or (
                "fraud" in raw_output.lower() and "not fraud" not in raw_output.lower()
            )

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
