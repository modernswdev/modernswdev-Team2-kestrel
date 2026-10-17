# 🧪 Compatibility Engine Computation Scratchpad

This file is an open sandbox area for brainstorming the math and logic rules for Issue #26. Please prefix your thoughts with your initials to track contributors of ideas before they get lost!

## ⚖️ Criteria Framework & Priority Weights

*   **[EL]:** Each dog profile will capture 4 distinct core parameters. To calculate a baseline personality match, the physical and behavioral traits are assigned weighted coefficients based on priority level:
    *   **Temperament (Weight 3):** Crucial for behavioral safety and ensuring smooth interactions.
    *   **Energy (Weight 2):** Essential for matching physical pacing and play stamina.
    *   **Size (Weight 1):** Secondary preference filter; different sizes can coexist safely if behaviors align.

## 📊 Metric 1–5 Scale Definitions

*   **[EL]:** To ensure database consistency and clean math evaluation, we will enforce explicit 1–5 option scales for our traits:

### 📐 Size Scale
*   **1:** X-Small
*   **2:** Small
*   **3:** Medium
*   **4:** Large
*   **5:** X-Large

### 🎭 Temperament Scale
*   **1 - Clingy:** Highly anxious or timid; sticks like velcro to handler, overwhelmed easily by other dogs.
*   **2 - Cautious:** Reserved and independent; takes a long time to warm up, prefers to observe from a distance.
*   **3 - Neutral:** Balanced and easygoing; doesn't mind other dogs, handles changing environments smoothly.
*   **4 - Outgoing:** Friendly and highly social; eagerly greets new dogs and loves group play.
*   **5 - Assertive:** Very bold and high-intensity; demands attention, takes charge in social settings, needs matching play styles.

### ⚡ Energy Scale
*   **1 - Low:** Prefers sleeping or lounging; gets tired quickly, needs minimal physical activity.
*   **2 - Gentle:** Enjoys short, casual walks; calm indoors, content with a relaxed pace.
*   **3 - Balanced:** Stamina for standard playtime or walks; has a steady "on/off" switch for activity.
*   **4 - Athletic:** Needs daily vigorous exercise like running or fetching; gets restless without an active outlet.
*   **5 - Intense:** Non-stop stamina; constantly on the move, requires intensive physical or mental jobs to tire out.

## 🗺️ ZIP Code & Proximity Calculations

*   **[EL]:** Distance will be evaluated by querying SQLite for coordinates and computing center-to-center raw mileage using external mapping libraries.
              I researched the best way to handle the distance math, and an AI assistant helped me verify that **`geopy`** is the industry-standard library for this. Instead of writing custom geometry formulas, we can use `geopy.distance.geodesic` to automatically compute mileage.
              Requirement: We will need to add `geopy` to our project's `requirements.txt` file so everyone can run `pip install geopy`.
*   **[EL]:** Calculated raw distances will map directly into 5 distinct geographic tiers:
    *   **Tier 1:** 0–15 miles
    *   **Tier 2:** 16–30 miles
    *   **Tier 3:** 31–60 miles
    *   **Tier 4:** 61–100 miles
    *   **Tier 5:** 101+ miles

## 🧠 Algorithmic Implementation & Computation Logic

*   **[EL]:** I propose a **Geographic Divisor Scaling System**. We calculate a baseline personality compatibility score using our traits, and then divide that percentage score directly by a scaling coefficient based on the distance tier to keep long-distance matches strictly below 60%.

### 1. Step 1: Calculate Personality Baseline %
*   We evaluate the absolute differences between Dog 1 and Dog 2 for Temperament, Energy, and Size.
*   Each difference is multiplied by its priority weight. The maximum possible penalty is 24 points.
*   `Total Penalty = (Temp_Diff * 3) + (Energy_Diff * 2) + (Size_Diff * 1)`
*   `Personality Baseline % = 100 - ((Total Penalty / 24) * 100)`

### 2. Step 2: Apply the Proximity Divisor Scale
*   The final percentage is determined by dividing the personality baseline by the geographic tier's divisor:
    *   **0–15 miles:** Divide by **1.0** (Stays at full value; close proximity carries no penalty)
    *   **16–30 miles:** Divide by **1.5** (Standard local drive commute)
    *   **31–60 miles:** Divide by **2.0** (Cuts final score exactly in half)
    *   **61–100 miles:** Divide by **2.5**
    *   **101+ miles:** Divide by **3.0** (Tanks long-distance scores down below 34%)
*   `Final Compatibility % = Personality Baseline % / Location Divisor`

## ⚠️ Fallback & Error Handling

*   **[EL]:** If a user inputs an out-of-state or invalid ZIP code, the SQLite coordinate lookup will return `None`. 
*   **[EL]:** To prevent a `TypeError` from crashing our Flask server during computation, the math engine should check for `None` coordinate values first and automatically assign a maximum **3.0** location divisor.

## 📥 Team Feedback & Contributions

*   *(Add your initials here to leave feedback or counter-proposals!)*

