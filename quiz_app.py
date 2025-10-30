import streamlit as st
import base64
import os

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Mechanical Quiz", page_icon="🎯", layout="centered")

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    page_bg = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        font-family: 'Poppins', sans-serif;
        color: #308695;
    }}
    h1, h2, h3, h4, h5, h6, p, label {{
        color: #308695 !important;
        font-family: 'Poppins', sans-serif !important;
    }}
    h1 {{
        font-size: 40px !important;
        font-weight: 700 !important;
        text-align: center !important;
        color: #308695 !important;
    }}
    label {{
        font-size: 40px !important;
        font-weight: 500 !important;
        color: #308695 !important;
    }}
    div[role="radiogroup"] > label {{
        font-size: 18px !important;
        color: #308695 !important;
    }}
    button[kind="primary"] {{
        background-color: #308695 !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-family: 'Poppins', sans-serif !important;
    }}
    .stSuccess {{
        color: white !important;
        background-color: #308695 !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Apply background
set_background("Quiz background.png")

# ---------------- LOGIN SYSTEM ----------------
approved_rolls = ["2025205023", "2025238723", "2025690359", "2025202525"]
admin_roll = "ADMIN"
admin_pass = "Pramod@123"
submitted_file = "submitted_users.txt"

# Create submission file if missing
if not os.path.exists(submitted_file):
    open(submitted_file, "w").close()

# Load submitted users
with open(submitted_file, "r") as f:
    submitted_users = f.read().splitlines()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_roll" not in st.session_state:
    st.session_state.user_roll = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "ready" not in st.session_state:
    st.session_state.ready = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🎓 Mechanical Quiz Login")

    roll = st.text_input("Enter Roll Number")
    password = st.text_input("Enter Password (Last 4 digits of Roll Number)", type="password")

    if st.button("Login"):
        if roll == admin_roll and password == admin_pass:
            st.session_state.logged_in = True
            st.session_state.user_roll = roll
            st.session_state.is_admin = True
            st.experimental_rerun()

        elif roll in approved_rolls and password == roll[-4:]:
            if roll in submitted_users:
                st.error("❌ You have already participated in this quiz.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_roll = roll
                st.session_state.is_admin = False
                st.success("✅ Login successful! Click 'Continue' to start the quiz.")
        else:
            st.error("❌ Invalid Roll Number or Password")

    # Continue button (only visible after successful login)
    if st.session_state.logged_in and not st.session_state.is_admin:
        if st.button("Continue"):
            st.session_state.ready = True
            st.experimental_rerun()
    st.stop()

# ---------------- ADMIN PANEL ----------------
if st.session_state.is_admin and not st.session_state.ready:
    st.title("👨‍💼 Admin Panel - Mechanical Quiz")
    st.write("✅ Logged in as Admin")

    with open(submitted_file, "r") as f:
        data = f.read().splitlines()
    if data:
        st.subheader("📋 Submitted Users:")
        for user in data:
            st.write(f"• {user}")
    else:
        st.info("No submissions yet.")

    if st.button("Reset Submissions"):
        open(submitted_file, "w").close()
        st.success("✅ Submission list cleared.")

    if st.button("Logout", key="admin_logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.experimental_rerun()
    st.stop()

# ---------------- MAIN QUIZ ----------------
if st.session_state.logged_in and (st.session_state.ready or st.session_state.is_admin == False):
    st.title("🎯 Welcome to the Mechanical Quiz")
    st.markdown(
        "<p style='text-align:center; font-size:20px; color:#308695;'>Answer the following questions carefully and click Submit when done!</p>",
        unsafe_allow_html=True
    )

    q1 = st.radio("⚙️ 1. Thermodynamics — Non-ideal Otto Cycle\n\nA four-stroke petrol engine operates on an Otto cycle with compression ratio 10. If specific heats vary with temperature, how does the efficiency compare with that calculated using constant specific heats?",
                  ["A. It increases", "B. It decreases", "C. It remains same", "D. Depends only on compression ratio"])

    q2 = st.radio("🧱 2. Strength of Materials — Eccentric Loading\n\nA short column has a circular cross-section and is eccentrically loaded such that the eccentricity equals half the radius. The maximum compressive stress occurs at the edge. The load is just sufficient to make stress zero at the farthest edge. Then, the eccentricity ratio e/r equals:",
                  ["A. 0.25", "B. 0.5", "C. 1", "D. 2"])

    q3 = st.radio("🔩 3. Machine Design — Fatigue\n\nA rotating steel shaft is under fully reversed bending stress. The endurance limit in rotating beam test is 250 MPa. If actual component has surface finish factor = 0.8, size factor = 0.85, and reliability factor = 0.9, then corrected endurance limit (MPa) ≈",
                  ["A. 153", "B. 175", "C. 191", "D. 250"])

    q4 = st.radio("⚡ 4. Fluid Mechanics — Boundary Layer\n\nFor laminar boundary layer flow over a flat plate, which statement is incorrect?",
                  ["A. Wall shear stress ∝ x⁻¹ᐟ²", "B. Boundary layer thickness ∝ x¹ᐟ²", "C. Local Nusselt number ∝ Rex¹ᐟ²", "D. Friction coefficient ∝ Rex⁻¹ᐟ²"])

    q5 = st.radio("🔧 5. Theory of Machines — Gyroscopic Couple\n\nA disc of mass m rotating at angular speed ω about its own axis is mounted on a precessing shaft with angular velocity Ω. The gyroscopic couple is:",
                  ["A. mωΩ", "B. IωΩ", "C. IΩ²", "D. mr²ωΩ"])

    q6 = st.radio("🔥 6. Heat Transfer — Radiation\n\nA small black body at 727°C is placed in a large evacuated chamber maintained at 27°C. Net heat loss rate per unit area is proportional to:",
                  ["A. T⁴", "B. T⁴ − Ts⁴", "C. T² − Ts²", "D. T − Ts"])

    q7 = st.radio("⚙️ 7. IC Engines — Mean Effective Pressure\n\nIf brake power (BP) and indicated power (IP) of an engine are 40 kW and 50 kW respectively, and mechanical efficiency = ?",
                  ["A. 80%", "B. 125%", "C. 50%", "D. 20%"])

    q8 = st.radio("🌀 8. Fluid Machinery — Cavitation\n\nWhich of the following parameters is used to check cavitation in a hydraulic turbine?",
                  ["A. Specific speed", "B. Thoma cavitation factor", "C. Flow ratio", "D. Head coefficient"])

    q9 = st.radio("🔩 9. Manufacturing — Tool Life Equation\n\nAccording to Taylor’s tool life equation VTⁿ = C, if cutting speed is reduced by 20%, tool life increases by:",
                  ["A. 25%", "B. 50%", "C. 100%", "D. Depends on n"])

    q10 = st.radio("🔬 10. Dynamics — Damped Vibration\n\nA mass–spring–damper system has ζ = 1.5. When displaced and released, the system will:",
                   ["A. Oscillate with reduced frequency", "B. Return to equilibrium without oscillation", "C. Never return to equilibrium", "D. Oscillate with increasing amplitude"])

    if st.button("Submit Quiz"):
        score = 0
        if q1.startswith("B."): score += 1
        if q2.startswith("B."): score += 1
        if q3.startswith("A."): score += 1
        if q4.startswith("C."): score += 1
        if q5.startswith("B."): score += 1
        if q6.startswith("B."): score += 1
        if q7.startswith("A."): score += 1
        if q8.startswith("B."): score += 1
        if q9.startswith("D."): score += 1
        if q10.startswith("B."): score += 1

        st.success(f"✅ Your score: {score}/10")

        # Save submission
        with open(submitted_file, "a") as f:
            f.write(f"{st.session_state.user_roll}\n")

        st.session_state.logged_in = False
        st.session_state.ready = False
        st.session_state.user_roll = None

        st.info("✅ Your responses have been recorded. You cannot attempt again.")

    if st.button("Logout", key="user_logout"):
        st.session_state.logged_in = False
        st.session_state.ready = False
        st.session_state.user_roll = None
        st.experimental_rerun()
