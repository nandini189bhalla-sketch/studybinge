import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# --- 1. PAGE SETTINGS ---
st.set_page_config(
    page_title="StudyBinge: AI Focus Optimizer",
    page_icon="📚",
    layout="wide"
)

# --- 2. INITIALIZE TEMPORARY MEMORY (SESSION STATE) ---
if 'custom_tasks' not in st.session_state:
    st.session_state['custom_tasks'] = []

# --- 3. THE DATASET ---
study_records = {
    'Difficulty':   [4,  8,  5,  9,  3,  7,  6,  2, 10,  5,  8,  4,  7,  9,  3],
    'Sleep':        [7.5,6.0,8.0,5.5,7.0,6.5,7.2,8.5,5.0,7.0,6.0,7.8,6.2,5.8,8.0],
    'ScreenTime':   [2.5,4.0,1.5,5.0,3.0,3.5,2.0,1.0,6.0,2.5,4.5,2.0,3.8,5.2,1.8],
    'Target':       [85, 90, 75, 95, 70, 88, 80, 65, 98, 82, 89, 78, 84, 92, 72],
    'FocusWindow':  [45, 30, 50, 25, 60, 35, 40, 75, 20, 45, 32, 48, 36, 24, 55]
}
df = pd.DataFrame(study_records)

# --- 4. TRAIN MACHINE LEARNING MODEL ---
X = df[['Difficulty', 'Sleep', 'ScreenTime', 'Target']]
y = df['FocusWindow']
model = LinearRegression()
model.fit(X, y)

# --- 5. SIDEBAR WORKSPACE ---
st.sidebar.title("🛠️ Session Workspace")

# Subject Profile Selector
st.sidebar.subheader("📖 Select Current Subject")
subject = st.sidebar.selectbox(
    "What are you studying right now?",
    ["Mathematics / Physics (High Analytical Load)", 
     "Chemistry / Biology (High Memorization Load)", 
     "Computer Science / IP (Practical Logic Load)", 
     "English / Humanities (Language & Reading Load)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Today's Target Tasks")
st.sidebar.write("Tick off your goals as you work:")

# The 3 Compulsory Base Tasks for Everyone
st.sidebar.checkbox("Complete Revision Notes")
st.sidebar.checkbox("Solve Previous Year Questions (PYQs)")
st.sidebar.checkbox("NCERT Exemplar Problems")

st.sidebar.markdown("---")
st.sidebar.write("📝 **Your Custom Tasks:**")

# Handle dynamic individual custom task deletion
to_remove = None
for index, task in enumerate(st.session_state['custom_tasks']):
    col_check, col_btn = st.sidebar.columns([4, 1])
    with col_check:
        st.checkbox(task, key=f"check_{index}")
    with col_btn:
        if st.button("🗑️", key=f"del_{index}"):
            to_remove = index

if to_remove is not None:
    st.session_state['custom_tasks'].pop(to_remove)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("➕ **Add Custom Task:**")
new_task = st.sidebar.text_input("Type task name & press Enter:", key="task_input")

if new_task and new_task not in st.session_state['custom_tasks']:
    st.session_state['custom_tasks'].append(new_task)
    st.rerun()


# --- 6. MAIN DASHBOARD ---
st.title("📚 StudyBinge: AI Focus & Break Optimizer")

# Credential Presentation Badges
col_name1, col_name2 = st.columns([2, 1])
with col_name1:
    st.markdown("### **Developed By:** Nandini Bhalla, Shrishti, Hannah , Adwaita, Purvi , Somya")
with col_name2:
    st.markdown("### **Class:** XII-B")

st.write("Input your metrics below to build a data-driven, burnout-free study schedule.")

# --- APPROACH 1: CONCEPTUAL BRIEF (PLACED AT THE TOP) ---
with st.expander("ℹ️ OVERVIEW: Our Conceptual Approach & Project Goal"):
    st.markdown("""
    ## *“Work hard in silence, work smart with data.”*
    ---
    ### 🛠️ Strategic Approach: Solution Design
    * **1️⃣ Identifying the Core Problem:** Generic study timers assume all students are identical. They completely ignore differences in subject types, sleep tracking, and mobile screen habits, causing early mental fatigue.
    * **2️⃣ Variable Extraction:** Our platform isolates four fundamental metrics to understand active mental capacity: Subject Difficulty, Sleep Restoration, Pre-existing Screen Fatigue, and Target Academic Milestones.
    * **3️⃣ Multi-Stream Inclusion:** Designed with a universal user footprint so that Science, Commerce, and Arts students can easily read, evaluate, and deploy customized schedules without technical confusion.
    * **4️⃣ Eliminating Burnout:** By converting personal lifestyle habits into actionable alerts, the app systematically protects learning consistency while optimizing peak memory retention.
    """)

st.markdown("---")

# 1. Input Metrics Form Section
st.subheader("🔮 1. Enter Your Session Metrics")
col_input1, col_input2 = st.columns(2)

with col_input1:
    difficulty = st.slider("Subject Difficulty (1 = Easy, 10 = Hard)", 1, 10, 5)
    sleep = st.number_input("Last Night's Sleep (Hours)", min_value=3.0, max_value=12.0, value=7.0, step=0.5)

with col_input2:
    screentime = st.number_input("Daily Phone Screen Time (Hours)", min_value=0.0, max_value=16.0, value=4.0, step=0.5)
    target = st.slider("Target Exam Score Aim (%)", 50, 100, 85)

st.markdown("---")

# 2. Real-Time Analytics Section
st.subheader("📊 2. Real-Time Analytics Dashboard")

if "Mathematics" in subject:
    subject_modifier = 1.3
elif "Chemistry" in subject:
    subject_modifier = 1.1
elif "Computer Science" in subject:
    subject_modifier = 1.0
else:
    subject_modifier = 0.8
    
fatigue_index = round(((difficulty * screentime) / (sleep + 0.1)) * subject_modifier, 2)

col_metric, col_chart = st.columns([1, 2])

with col_metric:
    st.write(" ")
    st.write(" ")
    st.metric(label="⚡ Your Live Fatigue Index Score", value=fatigue_index, delta="High Risk / Burnout Warning" if fatigue_index > 4 else "Optimal Focus State")

with col_chart:
    diff_levels = list(range(1, 11))
    fatigue_trends = [round(((d * screentime) / (sleep + 0.1)) * subject_modifier, 2) for d in diff_levels]
    
    chart_data = pd.DataFrame({
        'Subject Difficulty': diff_levels,
        'Fatigue Index': fatigue_trends
    })
    
    st.write(f"📈 **Fatigue Projection Chart for {subject.split(' (')[0]}:**")
    st.bar_chart(data=chart_data, x='Subject Difficulty', y='Fatigue Index', color='#FF4B4B')


# --- 7. AI PREDICTION ---
st.markdown("---")
if st.button("Calculate My Optimal Focus Window", type="primary"):
    user_input = np.array([[difficulty, sleep, screentime, target]])
    prediction = model.predict(user_input)[0]
    
    if "Mathematics" in subject:
        prediction = prediction * 0.85  
    elif "English" in subject:
        prediction = prediction * 1.15  
        
    final_streak = max(15, min(int(prediction), 90))
    
    st.subheader("🎯 Your AI-Generated Study Plan")
    st.metric(label="Optimal Focus Window", value=f"{final_streak} Minutes")
    
    if final_streak < 30:
        st.warning("⚠️ **High Fatigue / High Workload Detected:** Use a strict **25/5 Pomodoro Block** (25 mins study, 5 mins walk). No screens during breaks!")
    elif final_streak <= 50:
        st.info("📅 **Standard Focus Block:** Recommended **45-minute deep study session**, followed by a **10-minute physical recovery break**.")
    else:
        st.success("🚀 **Peak Cognitive State:** Engage in a **Deep Work Block of 60 to 75 minutes**. Follow up with a 15-minute complete mental disconnect.")


# --- APPROACH 2: THE SPECIAL PRACTICAL APPROACH (PLACED AT THE END) ---
st.markdown(" ")
st.markdown("---")
with st.expander("🛠️ TECHNICAL BRIEF: Our Special Practical Machine Learning Approach"):
    st.markdown("""
    ### ⚙️ Practical Approach: Data Science & Engineering Pipeline
    
    * **1️⃣ Matrix Initialization (The Training Set):**
        * Compiled an internal vector matrix `study_records` linking historical student productivity parameters directly with core focus outputs.
        * Features packed into dependent ($X$) arrays to store Difficulty, Sleep, ScreenTime, and Target metrics natively.
        
    * **2️⃣ Supervised Machine Learning Compilation:**
        * Imported the formal `LinearRegression` computational class structure directly out of the **Scikit-Learn (`sklearn`) library**.
        * Executed the `.fit(X, y)` method function to evaluate and assign numeric weight coefficients ($\omega$) and intercepts ($b$) to all lifestyle habits.
        
    * **3️⃣ Math Engine & Algorithmic Computations:**
        * Developed an active runtime calculator evaluating real-time inputs using a precise mathematical strain evaluation:
            $$\\text{Fatigue Index} = \\frac{\\text{Subject Difficulty} \\times \\text{Screen Time}}{\\text{Sleep}} \\times \\text{Subject Modifier}$$
        * Piped the resulting arrays instantly into a relational chart frame using `pandas.DataFrame` to map progressive fatigue curves dynamically.
        
    * **4️⃣ Custom Contextual Tuning:**
        * Structured hardcoded execution logic conditions to account for cognitive variations across different types of subjects ($1.3\\times$ penalty multiplier for heavy problem solving, $0.8\\times$ allowance modifier for language reading).
        
    * **5️⃣ Session-State Cache Arrays:**
        * Integrated Streamlit's structural `st.session_state` storage system to instantiate persistent checklist containers.
        * Created indexed row-column pairings containing customized data tags paired with absolute runtime deletion commands (`st.session_state.pop()`).
        
    * **6️⃣ UI Deployment Architecture:**
        * Bound the operational prediction models directly behind interactive web elements to transform complex data matrices into instant, automated study recommendations.
        
    ---
    """)
