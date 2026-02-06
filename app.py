import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-lite')

st.set_page_config(page_title="StyleSense Elite", page_icon="👠", layout="wide")

# --- 2. CUSTOM CSS (To make it look like a real app) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .style-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #FF4B4B; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&q=80")
    st.title("Stylist Settings")
    use_mock = st.toggle("🚀 Mock Mode (Instant)", value=True)
    st.divider()
    
    st.subheader("Your Profile")
    gender = st.radio("Style Category:", ["Masculine", "Feminine", "Unisex"])
    weather = st.selectbox("Current Weather:", ["Sunny & Warm", "Cold & Rainy", "Drafty/Autumn", "Snowy"])
    st.write("---")
    st.info("Current Model: Gemini 2.0 Flash-Lite")

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>👠 StyleSense Elite</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>AI-Powered Wardrobe Intelligence</h4>", unsafe_allow_html=True)

# Layout Columns
col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.subheader("📋 Outfit Details")
    user_item = st.text_input("Main Item:", placeholder="e.g., Beige Trench Coat")
    vibe = st.select_slider("Select Vibe Intensity:", 
                           options=["Super Casual", "Smart Casual", "Formal", "High Fashion"])
    
    base_color = st.color_picker("Main Item Color", "#D2B48C")
    accessories = st.multiselect("Include Accessories:", ["Watch", "Scarf", "Sunglasses", "Hat", "Bag"])
    
    generate_btn = st.button("✨ CURATE MY LOOK")

# --- 5. LOGIC & MOCK OUTPUTS ---
mock_responses = {
    "Super Casual": "Pair with relaxed joggers and chunky sneakers. Comfort is king here.",
    "Smart Casual": "Try slim-fit chinos and leather loafers. Perfect for a lunch meeting.",
    "Formal": "Match with tailored trousers and polished dress shoes. Keep the lines clean.",
    "High Fashion": "Go for contrast! Wide-leg pants and a statement belt. Think runway vibes."
}

with col_out:
    st.subheader("🎨 Your Curation")
    if generate_btn:
        if user_item:
            with st.spinner('Analyzing trends...'):
                if use_mock:
                    time.sleep(1)
                    st.balloons()
                    # Creating a "Card" look
                    st.markdown(f"""
                    <div class="style-card">
                        <h3>Recommended Style: {vibe}</h3>
                        <p><b>Top:</b> {user_item}</p>
                        <p><b>Bottoms:</b> Dark wash denim or tailored slacks</p>
                        <p><b>Shoes:</b> Minimalist leather sneakers</p>
                        <hr>
                        <p><i>Stylist Note: Since the weather is <b>{weather}</b>, layer with a thermal base!</i></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    try:
                        prompt = f"Stylist for {gender}. Suggest a full outfit for {user_item} ({base_color}) in {weather} weather. Vibe: {vibe}. Accessories: {accessories}."
                        response = model.generate_content(prompt)
                        st.markdown(f'<div class="style-card">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Quota Exceeded. Switch to Mock Mode! Error: {e}")
        else:
            st.warning("Please enter an item to start the curation.")
    else:
        st.info("Waiting for your input... Fill out the details on the left!")