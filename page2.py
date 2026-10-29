# page2.py
import streamlit as st
try:
    from geopy.distance import geodesic
except ImportError:
    st.error("Please run 'pip install geopy' in your terminal.")

st.title("📊 PawLink Match Analyzer")
st.write("Review profile grids and compute compatibility ratings between registered animals.")

# Check if at least two profiles exist in our temporary system memory clipboard
if "database" not in st.session_state or len(st.session_state.database) < 2:
    st.warning("⚠️ Please use the left menu to add at least TWO separate pets first!")
else:
    pet_list = list(st.session_state.database.keys())
    
    # Selection Row at the top
    st.markdown("### 🔍 Select Dogs to Compare")
    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        dog1_name = st.selectbox("First Dog", pet_list, index=0, key="select_dog1")
    with sel_col2:
        dog2_name = st.selectbox("Second Dog", pet_list, index=1 if len(pet_list) > 1 else 0, key="select_dog2")
        
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # PAWLINK HIGH-FIDELITY SIDE-BY-SIDE CARDS
    # -------------------------------------------------------------------------
    main_col1, main_col2 = st.columns(2)
    
    # Translation dictionaries to map 1-5 scale values back to your exact wireframe wording
    sizes = {1: "X-Small", 2: "Small", 3: "Medium", 4: "Large", 5: "X-Large"}
    temps = {1: "Clingy", 2: "Cautious", 3: "Neutral", 4: "Outgoing", 5: "Assertive"}
    energies = {1: "Low", 2: "Gentle", 3: "Balanced", 4: "Athletic", 5: "Energizer Bunny"}
    
    # --- DOG 1 PAWLINK VIEW ---
    with main_col1:
        d1 = st.session_state.database[dog1_name]
        
        # 1. Dynamic Photo Card Header (Using Dog 1's Name)
        st.markdown(f"#### 📸 {dog1_name}'s Photo")
        with st.container(border=True):
            if "photo" in d1 and d1["photo"] is not None:
                st.image(d1["photo"], use_container_width=True)
            else:
                st.info(f"🐕 No photo uploaded for {dog1_name}.")
        
        # 2. Profile Details Grid Container (Title Header Removed)
        with st.container(border=True):
            st.markdown(f"**ZIP Code:** {d1['zip']}")
            st.markdown(f"**Size:** {sizes.get(d1['traits']['size'], 'Unknown')}")
            st.markdown(f"**Temperament:** {temps.get(d1['traits']['temperament'], 'Unknown')}")
            st.markdown(f"**Energy Level:** {energies.get(d1['traits']['energy'], 'Unknown')}")

    # --- DOG 2 PAWLINK VIEW ---
    with main_col2:
        d2 = st.session_state.database[dog2_name]
        
        # 1. Dynamic Photo Card Header (Using Dog 2's Name)
        st.markdown(f"#### 📸 {dog2_name}'s Photo")
        with st.container(border=True):
            if "photo" in d2 and d2["photo"] is not None:
                st.image(d2["photo"], use_container_width=True)
            else:
                st.info(f"🐕 No photo uploaded for {dog2_name}.")
        
        # 2. Profile Details Grid Container (Title Header Removed)
        with st.container(border=True):
            st.markdown(f"**ZIP Code:** {d2['zip']}")
            st.markdown(f"**Size:** {sizes.get(d2['traits']['size'], 'Unknown')}")
            st.markdown(f"**Temperament:** {temps.get(d2['traits']['temperament'], 'Unknown')}")
            st.markdown(f"**Energy Level:** {energies.get(d2['traits']['energy'], 'Unknown')}")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # COMPUTATION ENGINE MATH
    # -------------------------------------------------------------------------
    if dog1_name == dog2_name:
        st.error("Please select two different animals to compare.")
    else:
        if st.button("🧬 Compute Compatibility Engine", type="primary", use_container_width=True):
            temp_diff = abs(d1["traits"]['temperament'] - d2["traits"]['temperament'])
            energy_diff = abs(d1["traits"]['energy'] - d2["traits"]['energy'])
            size_diff = abs(d1["traits"]['size'] - d2["traits"]['size'])
            
            total_penalty = (temp_diff * 3) + (energy_diff * 2) + (size_diff * 1)
            personality_baseline = 100.0 - ((total_penalty / 24.0) * 100.0)
            
            # Distance math using geopy as specified in scratchpad
            miles = geodesic(d1["coords"], d2["coords"]).miles
            if miles <= 15: divisor = 1.0
            elif miles <= 30: divisor = 1.5
            elif miles <= 60: divisor = 2.0
            elif miles <= 100: divisor = 2.5
            else: divisor = 3.0
            
            final_score = round(personality_baseline / divisor, 2)
            
            # Large dashboard success card
            st.success(f"## 🏆 PawLink Compatibility Rating: {final_score}%")
            st.info(f"📍 **Calculated Distance:** {round(miles, 2)} miles apart between ZIP {d1['zip']} and ZIP {d2['zip']}.")
