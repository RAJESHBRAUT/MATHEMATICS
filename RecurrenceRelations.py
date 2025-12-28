import streamlit as st
import random
import sympy as sp

# Configure page
st.set_page_config(page_title="Discrete Math: Recurrence Lab", layout="centered")

# Helper function to handle different Streamlit versions for rerunning
def trigger_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def generate_problem():
    # Generate distinct integer roots between -5 and 5 (excluding zero)
    r1 = random.choice([x for x in range(-5, 6) if x != 0])
    r2 = random.choice([x for x in range(-5, 6) if x != 0 and x != r1])
    
    # Recurrence: a_n = (r1+r2)a_{n-1} - (r1*r2)a_{n-2}
    s = r1 + r2
    t = -r1 * r2
    
    a0, a1 = random.randint(1, 10), random.randint(1, 10)
    return s, t, r1, r2, a0, a1

# Initialize Session State
if 'problem' not in st.session_state:
    st.session_state.problem = generate_problem()
    st.session_state.step1_done = False
    st.session_state.step2_done = False

s, t, r1, r2, a0, a1 = st.session_state.problem

st.title("🧮 Linear Recurrence Relations")
st.markdown("---")

# SECTION 1: THE PROBLEM
st.info(rf"""
**Current Problem:** Solve $a_n = {s}a_{{n-1}} {'+' if t >=0 else ''} {t}a_{{n-2}}$  
**Initial Conditions:** $a_0 = {a0}, a_1 = {a1}$
""")

# SECTION 2: CHARACTERISTIC ROOTS
st.subheader("Step 1: Characteristic Equation")
st.write(rf"Equation: $r^2 - ({s})r - ({t}) = 0$")


col1, col2 = st.columns(2)
u_r1 = col1.number_input("Root $r_1$:", step=1, key="root1")
u_r2 = col2.number_input("Root $r_2$:", step=1, key="root2")

if st.button("Verify Roots"):
    if set([u_r1, u_r2]) == set([r1, r2]):
        st.session_state.step1_done = True
        st.success(f"Correct! Roots are {r1} and {r2}.")
    else:
        st.error("Incorrect. Try factoring the quadratic again.")

# SECTION 3: CONSTANTS (Accepts Fractions)
if st.session_state.step1_done:
    st.markdown("---")
    st.subheader("Step 2: Solve for Constants A and B")
    st.write(rf"General Solution: $a_n = A({r1})^n + B({r2})^n$")
    st.latex(r"\begin{cases} A + B = " + str(a0) + r" \\ " + str(r1) + r"A + " + str(r2) + r"B = " + str(a1) + r" \end{cases}")

    # Logic to find constants for internal checking
    A_sym, B_sym = sp.symbols('A B')
    sol = sp.solve([A_sym + B_sym - a0, r1*A_sym + r2*B_sym - a1], [A_sym, B_sym])
    val_A, val_B = sol[A_sym], sol[B_sym]

    c1, c2 = st.columns(2)
    u_A_text = c1.text_input("Value of A (e.g., 20/3):", key="constA")
    u_B_text = c2.text_input("Value of B (e.g., 10/3):", key="constB")

    if st.button("Verify Constants"):
        try:
            user_A = sp.simplify(u_A_text)
            user_B = sp.simplify(u_B_text)
            if abs(float(user_A - val_A)) < 0.01 and abs(float(user_B - val_B)) < 0.01:
                st.session_state.step2_done = True
                st.success(f"Perfect! A = {val_A}, B = {val_B}")
            else:
                st.error("Check your algebraic solution.")
        except Exception:
            st.warning("Enter a valid number or fraction.")

# SECTION 4: VERIFICATION
if st.session_state.step2_done:
    st.markdown("---")
    st.subheader("Step 3: Verification")
    a2_rec = s*a1 + t*a0
    st.write(f"Calculate $a_2$ using your formula and check against recurrence result: **{a2_rec}**")
    u_a2_text = st.text_input("Your calculated $a_2$:", key="verify_a2")
    
    if st.button("Final Check"):
        try:
            if abs(float(sp.simplify(u_a2_text)) - a2_rec) < 0.01:
                st.balloons()
                st.success("Verification Successful!")
        except Exception:
            st.error("Invalid entry.")

if st.sidebar.button("New Problem"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    trigger_rerun()
