import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="StyleSense Pro v3", page_icon="💃", layout="wide")

# --- 2. SIDEBAR FOUNDATION (Move this up!) ---
with st.sidebar:
    st.title("🏗️ Foundation")
    # We define the season here first so the rest of the app can see it
    season = st.radio("Current Season", ["Spring", "Summer", "Fall", "Winter"], key="season_select")
    silhouette = st.selectbox("Body Silhouette", ["Tailored/Slim", "Oversized/Relaxed", "Athletic", "Classic Fit"])
    materials = st.multiselect("Preferred Materials", ["Leather", "Wool", "Silk", "Linen", "Denim", "Cotton"])
    st.divider()
    st.caption("v3.0 - Professional Personal Stylist")

# --- 3. DYNAMIC THEME LOGIC ---
# Now we use the variable 'season' we just created
colors = {"Spring": "#7C9473", "Summer": "#E9C46A", "Fall": "#A85832", "Winter": "#264653"}
season_color = colors.get(season, "#000000")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; }}
    .main-title {{ font-family: 'serif'; color: {season_color}; font-size: 3.5rem; font-weight: 700; }}
    .result-card {{ 
        background-color: #f8f9fa; padding: 30px; border-radius: 15px; 
        border-left: 10px solid {season_color}; margin-top: 20px;
        color: #333333;
    }}
    div.stButton > button:first-child {{
        background-color: {season_color}; color: white; border: none; width: 100%; height: 50px; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. AI SETUP ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key error! Please check your Secrets in Streamlit Cloud.")

# --- 5. MAIN STAGE ---
st.markdown(f'<h1 class="main-title">StyleSense {season}</h1>', unsafe_allow_html=True)
st.write("### Personal Wardrobe Consultation")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. The Creative Core")
    hero_piece = st.text_input("What is your 'Hero Piece'?", placeholder="e.g., A vintage oversized blazer")
    
    c1, c2 = st.columns(2)
    with c1:
        occasion = st.selectbox("The Occasion", ["Office/Corporate", "First Date", "Night Out", "Airport/Travel", "Coffee/Casual"])
    with c2:
        time_of_day = st.toggle("After Dark / Evening", value=False)
        
    st.subheader("2. The Aesthetic Goal")
    energy = st.select_slider("Energy Level", options=["Lazy/Comfort", "Balanced", "Powerful/Sharp"])
    
    c3, c4 = st.columns(2)
    with c3:
        aesthetic = st.selectbox("Aesthetic Filter", ["Old Money", "Streetwear", "Minimalist", "Grunge", "Preppy"])
    with c4:
        accent_color = st.color_picker("Accent Color Mood", "#D4AF37")

    if st.button("CURATE MY DOSSIER"):
        if not hero_piece:
            st.warning("Please enter a Hero Piece to begin.")
        else:
            with st.spinner("Styling your look..."):
                prompt = f"""
                Act as a professional high-fashion stylist. Build an elite outfit based on these:
                HERO: {hero_piece}. SEASON: {season}. SILHOUETTE: {silhouette}. MATERIALS: {materials}.
                OCCASION: {occasion}. TIME: {"Night" if time_of_day else "Day"}. ENERGY: {energy}.
                AESTHETIC: {aesthetic}. ACCENT COLOR: {accent_color}.
                
                Provide:
                1. THE LOOK: (A catchy name)
                2. THE CAPSULE: (List Top, Bottom, Shoes, Outerwear)
                3. STYLE STRATEGY: (Why this works for {season})
                4. ACCESSORIZER: (Jewelry/Bags)
                5. THE BIG NO-NO: (What to avoid)
                """
                try:
                    res = model.generate_content(prompt)
                    st.session_state['pro_output'] = res.text
                except:
                    st.session_state['pro_output'] = "API Quota full! Try again in a minute."

# --- 6. OUTPUT STAGE ---
with col2:
    if 'pro_output' in st.session_state:
        st.subheader("Your Styled Dossier")
        st.markdown(f'<div class="result-card">{st.session_state["pro_output"]}</div>', unsafe_allow_html=True)
        
        st.write("### Recommended Palette")
        cp1, cp2, cp3 = st.columns(3)
        cp1.color_picker("Base", "#FFFFFF", disabled=True, key="p1")
        cp2.color_picker("Secondary", "#000000", disabled=True, key="p2")
        cp3.color_picker("Accent", accent_color, disabled=True, key="p3")
    else:
        st.info("← Adjust your settings and click 'Curate' to see your styling dossier.")
        st.image("https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=800&q=80")
