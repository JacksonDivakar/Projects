import streamlit as st
import pymysql
from PIL import Image
import numpy as np
import tensorflow as tf

# ---------------------- CONFIGURATION ----------------------
st.set_page_config(page_title="Nutrition Tracker", layout="wide")

# Load the ML model
model_path = "/home/jackson-divakar/Documents/Calorie_Project/Model/best_model.keras"
model = tf.keras.models.load_model(model_path)

# Mapping for food labels
labels = {
    'apple_pie': 0, 'cheesecake': 1, 'chicken_curry': 2, 'french_fries': 3,
    'fried_rice': 4, 'hamburger': 5, 'hot_dog': 6, 'ice_cream': 7,
    'omelette': 8, 'pizza': 9, 'sushi': 10
}
inv_labels = {v: k for k, v in labels.items()}

# ---------------------- DATABASE CONNECTION ----------------------
connection = pymysql.connect(
    host='localhost',
    user='Jack',
    password='53787',
    database='calorie_project'
)
cursor = connection.cursor()

# ---------------------- SESSION STATE SETUP ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "required_values" not in st.session_state:
    # Initial values; these get updated after login/signup.
    st.session_state.required_values = {"calories": 0, "carbs": 0, "protein": 0, "fat": 0}

# ---------------------- HELPER FUNCTIONS ----------------------
def preprocess_image(image_file):
    """Open, resize, normalize, and expand dimensions of the image."""
    img = Image.open(image_file).resize((512, 512))
    img = np.array(img).astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)

def predict_labels(image_file):
    """Return the predicted food label for the uploaded image."""
    image_arr = preprocess_image(image_file)
    prediction = model.predict(image_arr)
    return inv_labels[np.argmax(prediction)]

def fetch_user_nutrition(user_id):
    """Fetch the user's current nutrition requirements."""
    query = "SELECT required_calories, required_carbs, required_protein, required_fat FROM user_nutrition WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def update_nutrition_in_db(user_id, new_vals):
    """Update the user's nutrition in the database."""
    update_query = """
        UPDATE user_nutrition
        SET required_calories = %s, required_carbs = %s, required_protein = %s, required_fat = %s
        WHERE user_id = %s
    """
    cursor.execute(update_query, (*new_vals, user_id))
    connection.commit()

# ---------------------- AUTHENTICATION UI ----------------------
def auth_ui():
    st.title("🔐 Welcome to Nutrition Tracker")
    tabs = st.tabs(["Login", "Sign Up"])
    
    with tabs[0]:
        st.subheader("🔑 Login")
        with st.form(key="login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Submit Login")
            
            if submit_login:
                query = "SELECT user_id, age, gender FROM user_data WHERE user_name = %s AND password_ = %s"
                cursor.execute(query, (username, password))
                data = cursor.fetchone()
                if data:
                    user_id, age, gender = data
                    st.session_state.user_id = user_id
                    st.session_state.logged_in = True
                    # Load the user's nutrition values into session state.
                    user_nutrition = fetch_user_nutrition(user_id)
                    if user_nutrition:
                        st.session_state.required_values = dict(
                            zip(["calories", "carbs", "protein", "fat"], user_nutrition)
                        )
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect credentials. Please try again or sign up.")
    
    with tabs[1]:
        st.subheader("📝 Create Account")
        with st.form(key="signup_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            gender_input = st.selectbox("Gender", ["M", "F"])
            age = st.number_input("Age", min_value=1, step=1)
            submit_signup = st.form_submit_button("Create Account")
            
            if submit_signup:
                gender = "Male" if gender_input == "M" else "Female"
                try:
                    # Insert the new user.
                    signup_query = "INSERT INTO user_data (user_name, password_, gender, age) VALUES (%s, %s, %s, %s)"
                    cursor.execute(signup_query, (new_username, new_password, gender, age))
                    connection.commit()
                    
                    # Retrieve the new user's ID.
                    cursor.execute("SELECT user_id FROM user_data WHERE user_name = %s AND password_ = %s", 
                                   (new_username, new_password))
                    user_id = cursor.fetchone()[0]
                    
                    # Get required nutrient values based on the user's age and gender.
                    nutrition_query = """
                        SELECT calories_min, carbs_min, protein_min, fat_min
                        FROM nutrients_data
                        WHERE age_min <= %s AND age_max >= %s AND gender = %s
                    """
                    cursor.execute(nutrition_query, (age, age, gender))
                    values = cursor.fetchone()
                    
                    # Insert the nutrition record.
                    insert_nutrition = """
                        INSERT INTO user_nutrition (user_id, required_calories, required_carbs, required_protein, required_fat)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_nutrition, (user_id, *values))
                    connection.commit()
                    
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.required_values = dict(
                        zip(["calories", "carbs", "protein", "fat"], values)
                    )
                    st.success("Account created successfully! You are now logged in.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Sign up failed: {e}")

# ---------------------- DASHBOARD UI ----------------------
def dashboard_ui():
    st.title("📁 Upload and Analyze Your Food Images")
    
    # Display KPI metrics at the top.
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🔥 Calories Left", int(st.session_state.required_values['calories']))
    kpi2.metric("🍚 Carbs Left", int(st.session_state.required_values['carbs']))
    kpi3.metric("🥚 Protein Left", int(st.session_state.required_values['protein']))
    kpi4.metric("🧈 Fat Left", int(st.session_state.required_values['fat']))
    
    st.markdown("---")
    
    # Allow user to upload multiple food images.
    uploaded_files = st.file_uploader("Upload food images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        # Make a copy of current nutrition values.
        new_nutrition = st.session_state.required_values.copy()
        # For storing predicted labels for display.
        predictions = []
        
        for uploaded_file in uploaded_files:
            # Display each image using a fixed width.
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=300)
            
            # Get prediction for this image.
            label = predict_labels(uploaded_file)
            predictions.append(label)
            st.success(f"🍽️ Predicted Food: {label}")
            
            # Fetch nutrient values for the predicted food.
            cursor.execute("SELECT calories, carbs, protein, fat FROM food_nutrients WHERE Food = %s", (label,))
            food_vals = cursor.fetchone()  # Tuple: (calories, carbs, protein, fat)
            
            if food_vals is not None:
                # Update each KPI by subtracting food nutrients, ensuring no negative values.
                new_nutrition["calories"] = max(0, new_nutrition["calories"] - food_vals[0])
                new_nutrition["carbs"]    = max(0, new_nutrition["carbs"]    - food_vals[1])
                new_nutrition["protein"]  = max(0, new_nutrition["protein"]  - food_vals[2])
                new_nutrition["fat"]      = max(0, new_nutrition["fat"]      - food_vals[3])
        
        # Update the database with the new nutrition values.
        update_nutrition_in_db(st.session_state.user_id, (new_nutrition["calories"], new_nutrition["carbs"],
                                                          new_nutrition["protein"], new_nutrition["fat"]))
        st.session_state.required_values = new_nutrition
        
        # Display final predictions and updated KPIs.
        st.info(f"Processed foods: {', '.join(predictions)}")
        st.success("Nutritional KPIs updated!")
    
    if st.button("🚪 Sign Out"):
        st.session_state.clear()
        st.rerun()

# ---------------------- MAIN FLOW ----------------------
if not st.session_state.logged_in:
    auth_ui()
else:
    dashboard_ui()

