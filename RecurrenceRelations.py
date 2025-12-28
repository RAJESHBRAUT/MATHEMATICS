import streamlit as st
import random
import sympy as sp

# Configure page
st.set_page_config(page_title="Discrete Math: Recurrence Lab", layout="centered")

# Helper function for version-safe rerun
def trigger_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def generate_problem():
    # Roots r1, r2 between -5 and 5 (distinct and non-zero)
    r1 = random.choice([x for x in range(-5, 6) if x != 0])
    r2 = random.choice([x for x in range(-5, 6) if x != 0 and x != r1])
    
    s = r1 + r2
    t = -r1 * r2
    
    # Random initial conditions
    a0 = random.randint(1, 10)
    a1 = random.randint(1, 10)
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
**Problem:** Solve $a_n = {s}a_{{n-1}} {'+' if t >=0 else ''} {t}a_{{n-2}}$  
**Initial Conditions:** $a_0 = {a0}, a_1 = {a1}$
""")

# SECTION 2: ROOTS
st.subheader("Step 1: Characteristic Equation & Roots")
st.write(rf"The characteristic equation is: $r^2 - ({s})r - ({t}) = 0$")



col1, col2 = st.columns(2)
# Using value=0 to ensure inputs are initialized
u_r1 = col1.number_input("Enter root $r_1$:", step=1, key="root1")
u_r2 = col2.number_input("Enter root $r_2$:", step=1, key="root2")

if st.button("Verify Roots"):
    if set([u_r1, u_r2]) == set([r1, r2]):
        st.session_state.step1_done = True
        st.success(f"Correct! The roots are {r1} and {r2}.")
    else:
        st.error("Incorrect roots. Factoring the quadratic: $(r - r_1)(r - r_2) = 0$.")

# SECTION 3: CONSTANTS
if st.session_state.step1_done:
    st.markdown("---")
    st.subheader("Step 2: Find Arbitrary Constants A and B")
    st.write(rf"General Solution: $a_n = A({r1})^n + B({r2})^n$")
    
    # Standard LaTeX cases environment for initial conditions
    st.latex(r"\begin{cases} A + B = " + str(a0) + r" \\ " + str(r1) + r"A + " + str(r2) + r"B = " + str(a1) + r" \end{cases}")

    

    # Calculate actual constants using Sympy (preserving fractions)
    A_sym, B_sym = sp.symbols('A B')
    sol = sp.solve([A_sym + B_sym - a0, r1*A_sym + r2*B_sym - a1], [A_sym, B_sym])
    val_A = sol[A_sym]
    val_B = sol[B_sym]

    st.write("Enter values (You can use fractions like 20/3 or decimals like 6.66)")
    c1, c2 = st.columns(2)
    u_A_text = c1.text_input("Value of A:", key="constA")
    u_B_text = c2.text_input("Value of B:", key="constB")

    if st.button("Verify Constants"):
        try:
            # sp.simplify converts text "20/3" into exact math fraction
            user_A = sp.simplify(u_A_text)
            user_B = sp.simplify(u_B_text)
            
            # Using float subtraction to allow small margin of error for decimals
            if abs(float(user_A - val_A)) < 0.01 and abs(float(user_B - val_B)) < 0.01:
                st.session_state.step2_done = True
                st.success(f"Correct! A = {val_A} and B = {val_B}")
            else:
                st.error(f"Try again. Hint: Set up your equations using initial conditions.")
        except:
            st.warning("Please enter a valid number or fraction (e.g., 5, 6.66, or 20/3).")

# SECTION 4: VERIFICATION
if st.session_state.step2_done:
    st.markdown("---")
    st.subheader("Step 3: Final Verification (n=2)")
    
    a2_rec = s*a1 + t*a0
    st.write(rf"**Method 1 (Recurrence):** $a_2 = {s}({a1}) {'+' if t >=0 else ''} {t}({a0}) = {a2_rec}$")
    
    
    
    u_a2_text = st.text_input("Method 2: Calculate $a_2$ using your Formula:", key="verify_a2")
    
    if st.button("Final Verification"):
        try:
            user_a2 = sp.simplify(u_a2_text)
            if abs(float(user_a2 - a2_rec)) < 0.01:
                st.balloons()
                st.success(f"Verified! Both methods yield $a_2 = {a2_rec}$.")
            else:
                st.error(f"Mismatch! Formula gives {float(user_a2)}, but Recurrence gives {a2_rec}.")
        except:
            st.error("Invalid entry. Please enter a numerical value.")

# RESET BUTTON (Side Bar)
if st.sidebar.button("Generate New Problem"):
    # Clearing session state to reset the UI completely
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    trigger_rerun()
