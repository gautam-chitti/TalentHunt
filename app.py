# app.py
import streamlit as st
from streamlit_extras.app_logo import add_logo

# Page Configuration
st.set_page_config(
    page_title="Welcome to TalentScout AI",
    page_icon="🤖",
    layout="centered"
)

# Logo and Styling 

st.markdown("""
    <style>
        .stButton>button {
            height: 3em;
            width: 100%;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# Main  Page 
st.title("Welcome to TalentScout AI 🤖")
st.write("Your intelligent partner in technical screening.")

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
   
    st.markdown("---")
    st.subheader("I am a...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Candidate (Take the Screening Test)", type="primary"):
            st.switch_page("pages/1_Take_Screening_Test.py")
    
    with col2:
      
        with st.expander("Administrator (Sign In)"):
            with st.form("admin_login_form"):
                email = st.text_input("Email", placeholder="Enter Your Email")
                password = st.text_input("Password", type="password", placeholder="Enter Your Password")
                submitted = st.form_submit_button("Sign In")

                if submitted:
                    # Hardcoded credentials for this assignment
                    if email == "admin@talenthunt.com" and password == "admin123":
                        st.session_state.admin_logged_in = True
                        st.success("Signed in successfully!")
                        st.rerun() 
                    else:
                        st.error("Invalid email or password.")
else:
    # Admin View 
    st.success("You are signed in as an administrator.")
    st.write("You can now access the admin dashboard from the sidebar.")
    
    if st.button("Sign Out"):
        st.session_state.admin_logged_in = False
        st.success("You have been signed out.")
        st.rerun()

# Hide pages from sidebar based on login status
if not st.session_state.admin_logged_in:
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] ul li:nth-child(2) {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)