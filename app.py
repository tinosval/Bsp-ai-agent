import streamlit as st
import os
from agent import generate_bsp
from document_gen import generate_word_document

st.set_page_config(
    page_title="BSP AI Agent",
    page_icon="📋",
    layout="centered"
)

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0046b5;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #003494;
        color: white;
    }
    .header-box {
        background: linear-gradient(135deg, #0046b5, #0099cc);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0046b5;
        margin-bottom: 20px;
        color: #000000 !important;
    }
    .success-box {
        background-color: #e8f8e8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #fff8e8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin-bottom: 20px;
    }
    footer {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
    <div class="header-box">
        <h1>📋 BSP AI Agent</h1>
        <p style="font-size: 18px; margin: 0;">
            Behaviour Support Plan Generator
        </p>
        <p style="font-size: 14px; margin-top: 10px; opacity: 0.9;">
            Powered by Internal Resource Documents Only
        </p>
    </div>
""", unsafe_allow_html=True)

# ===== INFO BOX =====
st.markdown("""
 <div class="info-box" style="color: #000000;">
        <strong>ℹ️ How it works:</strong> Enter client details below. 
        The AI agent will search ONLY the internal resource document 
        and generate a professional BSP automatically. 
        If a diagnosis is not found, it will be flagged for manual review.
    </div>
""", unsafe_allow_html=True)

# ===== CHECK KNOWLEDGE BASE =====
if not os.path.exists("./knowledge_base_db"):
    st.error(
        "Knowledge base not found. "
        "Please run: python build_kb.py"
    )
    st.stop()

st.markdown("### 👤 Client Information")

# ===== FORM =====
with st.form("bsp_form", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:
        client_name = st.text_input(
            "Client Full Name *",
            placeholder="e.g. John Smith"
        )
        diagnosis = st.text_input(
            "Primary Diagnosis *",
            placeholder="e.g. Schizophrenia"
        )
        support_worker = st.text_input(
            "Support Worker Name",
            placeholder="e.g. Jane Doe"
        )

    with col2:
        plan_type = st.selectbox(
            "Plan Type *",
            options=["interim", "comprehensive"],
            format_func=lambda x: x.capitalize()
        )
        coordinator = st.text_input(
            "BSP Coordinator",
            placeholder="e.g. Bob Jones"
        )
        ndis_number = st.text_input(
            "NDIS Number",
            placeholder="e.g. 123456789"
        )

    st.markdown("---")
    st.markdown("### ⚠️ Behaviours of Concern")

    behaviours = st.text_area(
        "Describe the behaviours of concern *",
        placeholder="e.g. Verbal aggression towards support workers during personal care routines",
        height=100
    )

    col3, col4 = st.columns(2)

    with col3:
        frequency = st.selectbox(
            "How often do behaviours occur? *",
            options=[
                "Multiple times daily",
                "Daily",
                "Several times per week",
                "Weekly",
                "Fortnightly",
                "Monthly",
                "Rarely"
            ]
        )

    with col4:
        intensity = st.selectbox(
            "Intensity level *",
            options=["Low", "Moderate", "High", "Severe"]
        )

    triggers = st.text_area(
        "Known triggers",
        placeholder="e.g. Loud noises, unexpected changes to daily routine",
        height=80
    )

    additional_info = st.text_area(
        "Additional information",
        placeholder="Any other relevant information about the client",
        height=80
    )

    st.markdown("---")

    submitted = st.form_submit_button(
        "🚀 Generate BSP",
        use_container_width=True,
        type="primary"
    )

# ===== PROCESS =====
if submitted:
    if not client_name:
        st.error("Please enter the client name")
    elif not diagnosis:
        st.error("Please enter the primary diagnosis")
    elif not behaviours:
        st.error("Please describe the behaviours of concern")
    else:
        client_details = {
            "name": client_name,
            "diagnosis": diagnosis,
            "behaviours": behaviours,
            "frequency": frequency,
            "intensity": intensity,
            "triggers": triggers if triggers else "Not specified",
            "additional_info": additional_info if additional_info else "None",
            "support_worker": support_worker if support_worker else "Not specified",
            "coordinator": coordinator if coordinator else "Not specified",
            "ndis_number": ndis_number if ndis_number else "Not specified"
        }

        with st.spinner("Generating BSP - please wait..."):

            progress = st.progress(0)
            status = st.empty()

            status.text("Step 1 of 3: Searching internal resource document...")
            progress.progress(25)

            result = generate_bsp(client_details, plan_type)
            progress.progress(60)

            if result["flag"]:
                progress.progress(100)
                status.empty()
                st.markdown("""
                    <div class="warning-box">
                        <strong>⚠️ Diagnosis Flagged</strong><br>
                        This diagnosis was not found in the internal 
                        resource document.
                    </div>
                """, unsafe_allow_html=True)
                st.warning(result["message"])
                st.info(
                    "Action Required: Please either review this BSP "
                    "manually or update the internal resource document "
                    "to include this diagnosis."
                )

            elif result["success"]:
                status.text("Step 2 of 3: Creating Word document...")
                progress.progress(80)

                output_path, filename = generate_word_document(result)
                progress.progress(100)
                status.empty()

                st.markdown("""
                    <div class="success-box">
                        <strong>✅ BSP Generated Successfully!</strong><br>
                        Your Behaviour Support Plan is ready to download.
                        Please review before implementation.
                    </div>
                """, unsafe_allow_html=True)

                st.success(
                    f"BSP generated for {client_name} - "
                    f"{plan_type.capitalize()} Plan"
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 Download BSP Word Document",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )

                with col_b:
                    st.info(
                        f"Plan Type: {plan_type.capitalize()}\n\n"
                        f"Sections: {len(result['content'])}\n\n"
                        f"File: {filename}"
                    )

                st.markdown("---")
                st.markdown("### 📄 Preview Generated Content")

                for i, (section_name, section_content) in enumerate(
                    result["content"].items(), 1
                ):
                    with st.expander(f"Section {i}: {section_name}"):
                        st.write(section_content)

            else:
                st.error("Error: " + result["message"])

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
    <footer>
        <p>
            BSP AI Agent | Built by Valentine Shedrach | 
            Powered by OpenAI GPT & LangChain
        </p>
        <p>
            ⚠️ All generated BSPs use internal resource documents only. 
            Clinical review required before implementation.
        </p>
    </footer>
""", unsafe_allow_html=True)