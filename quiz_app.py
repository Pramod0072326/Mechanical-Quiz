import streamlit as st
import base64
import os

# ---------------- CONFIG ----------------
APP_TITLE = "🎯 Welcome to the Mechanical Quiz"
BACKGROUND_IMAGE = "Quiz background.png"

APPROVED_FILE = "approved_users.txt"
SUBMITTED_FILE = "submitted_users.txt"

ADMIN_PASSWORD = "Pradmin@123"

# ---------------- HELPERS ----------------
def set_background(image_file):
    encoded = ""
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
    except FileNotFoundError:
        encoded = ""

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
    }}
    label {{
        font-size: 18px !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)


def ensure_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            pass


def read_list(path):
    ensure_file(path)
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def write_list(path, lst):
    with open(path, "w") as f:
        for item in lst:
            f.write(f"{item}\n")


def append_to_file(path, value):
    ensure_file(path)
    with open(path, "a") as f:
        f.write(f"{value}\n")


def remove_from_file(path, value):
    lst = read_list(path)
    if value in lst:
        lst.remove(value)
        write_list(path, lst)
        return True
    return False


def is_admin_login(pwd):
    return pwd == ADMIN_PASSWORD


def is_valid_user_login(roll, pwd, approved_list):
    return roll in approved_list and len(pwd) == 4 and roll.endswith(pwd)


# ---------------- INITIAL SETUP ----------------
st.set_page_config(page_title="Mechanical Quiz", page_icon="🎯", layout="centered")
set_background(BACKGROUND_IMAGE)

ensure_file(APPROVED_FILE)
ensure_file(SUBMITTED_FILE)

for key, val in {
    "logged_in": False,
    "is_admin": False,
    "ready": False,
    "admin_authenticated": False,
    "show_admin_login": False,
    "user_roll": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

approved_users = read_list(APPROVED_FILE)
submitted_users = read_list(SUBMITTED_FILE)

# ---------------- ADMIN BUTTON ----------------
if st.button("Admin", key="admin_btn", help="Admin Login", use_container_width=False):
    st.session_state.show_admin_login = not st.session_state.show_admin_login
    st.session_state.admin_authenticated = False
    st.rerun()

# ---------------- ADMIN LOGIN ----------------
if st.session_state.show_admin_login and not st.session_state.admin_authenticated:
    st.markdown("### 🔐 Admin Access")
    admin_pwd = st.text_input("Enter Admin Password", type="password", key="admin_pwd")
    if st.button("Login as Admin", key="admin_login_btn"):
        if is_admin_login(admin_pwd):
            st.session_state.admin_authenticated = True
            st.session_state.is_admin = True
            st.session_state.logged_in = True
            st.session_state.show_admin_login = False
            st.success("✅ Admin login successful!")
            st.rerun()
        else:
            st.error("Incorrect password")

# ---------------- ADMIN PANEL ----------------
if st.session_state.admin_authenticated and st.session_state.is_admin:
    st.title("👨‍💼 Admin Panel - Mechanical Quiz")

    approved_users = read_list(APPROVED_FILE)
    submitted_users = read_list(SUBMITTED_FILE)

    st.subheader("📋 Approved Participants")
    st.write("\n".join(approved_users) if approved_users else "No approved participants.")

    st.markdown("---")
    st.subheader("📌 Submitted Participants")
    st.write("\n".join(submitted_users) if submitted_users else "No submissions yet.")

    st.markdown("---")
    st.subheader("🔧 Admin Actions")

    new_roll = st.text_input("Add new roll number", key="new_roll")
    if st.button("Add Roll Number", key="add_roll_btn"):
        if new_roll.strip():
            approved_users = read_list(APPROVED_FILE)
            if new_roll not in approved_users:
                append_to_file(APPROVED_FILE, new_roll.strip())
                st.success(f"✅ {new_roll} added to approved list.")
            else:
                st.info("This roll is already approved.")
        else:
            st.error("Enter a roll number.")

    reset_roll = st.text_input("Enter roll number to reset participation", key="reset_roll")
    if st.button("Reset Participation", key="reset_part_btn"):
        if reset_roll.strip():
            ok = remove_from_file(SUBMITTED_FILE, reset_roll.strip())
            if ok:
                st.success(f"✅ {reset_roll} can now reattempt the quiz.")
            else:
                st.info(f"{reset_roll} was not in submitted list.")
        else:
            st.error("Enter a roll number.")

    if st.button("Logout Admin", key="logout_admin_btn"):
        for key in ["logged_in", "is_admin", "admin_authenticated", "show_admin_login", "user_roll", "ready"]:
            st.session_state[key] = False
        st.rerun()

    st.stop()

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.title("🎓 Mechanical Quiz Login")
    st.markdown("<small style='color:#308695'>Enter your Roll Number and Password (last 4 digits of your roll).</small>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        input_roll = st.text_input("Roll Number", key="input_roll")
    with col2:
        input_pwd = st.text_input("Password (last 4 digits)", type="password", key="input_pwd")

    if st.button("Login", key="login_btn"):
        roll = input_roll.strip()
        pwd = input_pwd.strip()
        approved_users = read_list(APPROVED_FILE)
        submitted_users = read_list(SUBMITTED_FILE)

        if is_valid_user_login(roll, pwd, approved_users):
            if roll in submitted_users:
                st.error("❌ You have already participated in this quiz.")
            else:
                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.session_state.ready = False
                st.session_state.user_roll = roll
                st.success("✅ Login successful. Click Continue to start the quiz.")
        else:
            st.error("❌ Invalid Roll Number or Password.")

    st.stop()

# ---------------- CONTINUE BUTTON ----------------
if st.session_state.logged_in and not st.session_state.is_admin:
    if not st.session_state.ready:
        if st.button("Continue", key="continue_btn"):
            st.session_state.ready = True
            st.rerun()
        st.stop()

# ---------------- QUIZ PAGE ----------------
if st.session_state.logged_in and not st.session_state.is_admin and st.session_state.ready:
    st.title(APP_TITLE)
    st.markdown("<p style='text-align:center; font-size:20px; color:#308695;'>Answer the following questions carefully and click Submit when done!</p>", unsafe_allow_html=True)

    questions = [
        ("1. For a real gas obeying van der Waals equation, the correction term a/v² accounts for:",
         ["(A) Volume occupied by gas molecules", "(B) Intermolecular attractions", "(C) Elastic collisions", "(D) Random motion of molecules"],
         "(B) Intermolecular attractions"),

        ("2. During isentropic compression, the temperature rise is maximum when:",
         ["(A) Gas has higher specific heat ratio (γ)", "(B) Gas has lower γ", "(C) Both have same γ", "(D) Depends only on pressure ratio"],
         "(A) Gas has higher specific heat ratio (γ)"),

        ("3. If a solid circular shaft and a hollow shaft of same material and weight transmit equal torque, then:",
         ["(A) Both have same shear stress", "(B) Hollow shaft has higher shear stress", "(C) Hollow shaft has lesser shear stress", "(D) Cannot be compared"],
         "(C) Hollow shaft has lesser shear stress"),
        
        ("4. Critical speed of a rotating shaft is independent of:",
         ["(A) Mass of the shaft", "(B) Shaft diameter", "(C) Type of support", "(D) Distribution of mass"], "(C) Type of support"),

        ("5. The maximum efficiency of a jet propulsion engine occurs when:",
         ["(A) Jet velocity = Flight velocity", "(B) Jet velocity = 0", "(C) Jet velocity = 2 × Flight velocity", "(D) Flight velocity = 0"], "(C) Jet velocity = 2 × Flight velocity"),

        ("6. In heat exchangers, the log mean temperature difference (LMTD) is used because:",
         ["(A) Heat capacity rate is constant", "(B) Temperature difference varies linearly", "(C) Temperature difference varies exponentially", "(D) Heat flow is uniform"], "(C) Temperature difference varies exponentially"),

        ("7. When the Mach number = 1, the flow is said to be:",
         ["(A) Supersonic", "(B) Subsonic", "(C) Sonic", "(D) Hypersonic"], "(C) Sonic"),

        ("8. In hydraulic turbines, cavitation occurs when:",
         ["(A) Pressure at any point falls below vapor pressure", "(B) Velocity increases beyond limit", "(C) Flow becomes turbulent", "(D) Air enters with water"], "(A) Pressure at any point falls below vapor pressure"),

        ("9. In Euler’s column theory, the crippling load is inversely proportional to:",
         ["(A) Length", "(B) Length²", "(C) Diameter", "(D) Modulus of elasticity"], "(B) Length²"),

        ("10. Thermal conductivity of most liquids:",
         ["(A) Increases with rise in temperature", "(B) Decreases with rise in temperature", "(C) Remains constant", "(D) Changes irregularly"], "(B) Decreases with rise in temperature"),

        ("11. For a double acting reciprocating compressor, the volumetric efficiency is:",
         ["(A) Less than single acting", "(B) Greater than single acting", "(C) Equal to single acting", "(D) Independent of type"], "(B) Greater than single acting"),

        ("12. In epicyclic gear trains, the velocity ratio is inversely proportional to:",
         ["(A) Number of teeth on fixed gear", "(B) Number of teeth on planet gear", "(C) Number of teeth on sun gear", "(D) Module of gears"], "(A) Number of teeth on fixed gear"),

        ("13. A Rankine cycle efficiency increases if:",
         ["(A) Condenser pressure increases", "(B) Condenser pressure decreases", "(C) Boiler pressure decreases", "(D) Both (A) and (B)"], "(B) Condenser pressure decreases"),

        ("14. In metal cutting, the chip thickness ratio (r) is always:",
         ["(A) Greater than 1", "(B) Less than 1", "(C) Equal to 1", "(D) Infinite"], "(B) Less than 1"),

        ("15. Mohr’s circle for pure shear stress will be a circle having its center at:",
         ["(A) Origin", "(B) σ-axis at τ/2", "(C) σ = 0, τ = 0", "(D) σ = τ"], "(C) σ = 0, τ = 0"),

    ]

    with st.form(key="quiz_form"):
        user_answers = []
        for idx, (q, choices, _) in enumerate(questions, start=1):
            user_choice = st.radio(f"{q}", choices, key=f"q_{idx}")
            user_answers.append(user_choice)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        score = 0
        for ans, (_, _, correct) in zip(user_answers, questions):
            if ans == correct:
                score += 1

        if st.session_state.user_roll not in read_list(SUBMITTED_FILE):
            append_to_file(SUBMITTED_FILE, st.session_state.user_roll)

        st.success(f"✅ Your score: {score}/{len(questions)}")
        st.info("Your attempt has been recorded. You cannot participate again unless admin resets your entry.")

        for key in ["logged_in", "ready", "user_roll"]:
            st.session_state[key] = False

    if st.button("Logout", key="student_logout_btn"):
        for key in ["logged_in", "ready", "user_roll"]:
            st.session_state[key] = False
        st.rerun()

