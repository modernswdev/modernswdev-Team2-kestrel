# page1.py
import streamlit as st

st.title("🐾 Create a Pet Profile")
st.write("Enter your dog's details to register them into the system.")

# Ensure our global system memory exists
if "database" not in st.session_state:
    st.session_state.database = {}

with st.form("pet_profile_form"):
    pet_name = st.text_input("Pet Name", placeholder="e.g., Buster, Daisy, Luna")
    
    # 📸 Featured Dog Photo file uploader
    st.subheader("📷 Featured Dog Photo")
    uploaded_photo = st.file_uploader("Upload a picture of your pet", type=["jpg", "jpeg", "png"])
    
    # 📐 Physical Profile matching scales with your specific weight thresholds
    st.subheader("📐 Physical Profile")
    size_label = st.selectbox("Select Dog Size & Weight", [
        "1 - X-Small (Under 10 lbs)", 
        "2 - Small (10–25 lbs)", 
        "3 - Medium (26–60 lbs)", 
        "4 - Large (61–90 lbs)", 
        "5 - X-Large (Over 90 lbs)"
    ])
    size_value = int(size_label.split(" - ")[0])

    # 🎭 Behavioral & Personality Profile metric option scales
    st.subheader("🎭 Behavioral & Personality Profile")
    temp_label = st.selectbox("Temperament Style", [
        "1 - Clingy (Highly anxious, timid)", 
        "2 - Cautious (Reserved, independent)",
        "3 - Neutral (Balanced, easygoing)", 
        "4 - Outgoing (Friendly, highly social)",
        "5 - Assertive (Very bold, high-intensity)"
    ])
    temp_value = int(temp_label.split(" - ")[0])

    # ⚡ Energy and play pacing scale
    energy_label = st.selectbox("Energy & Stamina Level", [
        "1 - Low (Prefers lounging, needs minimal activity)", 
        "2 - Gentle (Enjoys short walks, calm indoors)",
        "3 - Balanced (Steady 'on/off' switch for activity)", 
        "4 - Athletic (Needs daily vigorous exercise like running)",
        "5 - Intense (Non-stop stamina, requires intensive physical jobs)"
    ])
    energy_value = int(energy_label.split(" - ")[0])

    # 🗺️ Geographic Location 5-digit ZIP format
    st.subheader("🗺️ Geographic Location")
    zip_code = st.text_input("Standard 5-digit ZIP Code", max_chars=5, placeholder="e.g., 72103")

    # Correct submission trigger token to resolve engine crash
    submitted = st.form_submit_button("💾 Save Profile", type="primary")

if submitted:
    if not pet_name or not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        st.error("❌ Please enter a valid pet name and a standard 5-digit ZIP code.")
    else:
        # Mocking backend coordinate data arrays for testing calculation pipelines
        mock_lat = 35.7796 + (len(pet_name) * 0.01)
        mock_lon = -78.6382 - (int(zip_code[-1]) * 0.01)
        
        # Storing comprehensive target data structures to st.session_state
        st.session_state.database[pet_name] = {
            "traits": {"temperament": temp_value, "energy": energy_value, "size": size_value},
            "zip": zip_code,
            "coords": (mock_lat, mock_lon),
            "photo": uploaded_photo
        }
        st.success(f"🎉 Saved {pet_name} (ZIP: {zip_code}) to temporary memory! Registered: {list(st.session_state.database.keys())}")
