# Project Repository: Data Science, DL, ML & Time Series Analysis

Welcome to the **Project Repository**! This repository is organized into several folders, each dedicated to different aspects of data science and modeling. Whether you are interested in Exploratory Data Analysis, Deep Learning experiments, traditional Machine Learning methods, or Time Series Analysis, you will find sample projects, notebooks, and scripts here to help guide your learning and development.


## Detailed Folder Overviews

### EDA  
This folder includes exploratory data analysis projects, such as:
- **Notebooks** that describe initial data exploration, visualization, data cleaning, and feature selection.
- **Scripts** that perform quick data transformations and plot generation.
- The EDA section helps you understand the underlying structure of your datasets before deploying any machine learning models.

### DL  
In the Deep Learning folder, you will find:
- **Model definitions and training scripts** for various neural network architectures (e.g., CNN, RNN).
- **Notebooks** that include experiments, parameter tuning, and performance evaluation.
- You can also locate pre-trained models used for projects such as food classification or image recognition.

### ML  
The Machine Learning folder features projects related to:
- **Supervised and unsupervised learning algorithms**, including implementation code.
- **Notebooks** that focus on feature engineering, model training, cross-validation, and performance metrics.
- This section is designed to illustrate the differences between traditional ML methods and modern DL approaches.

### Time Series Analysis  
This folder is dedicated to time series work such as:
- **Jupyter Notebooks** demonstrating seasonal decompositions, forecasting (using ARIMA, Prophet, etc.), and anomaly detection.
- **Python scripts** that implement time series models and visualize trends over time.
- If you’re working with temporal data, this folder provides useful examples and starting points.

### Nutrition Tracker Project  
This is a full-stack project where you can:
- Upload food images via a **Streamlit web interface**.
- Use a Deep Learning model (stored in the `Model/` folder) to predict food labels.
- Automatically update nutritional KPIs (calories, carbohydrates, protein, fats) based on model predictions.
- The project integrates **PyMySQL** for database operations, **TensorFlow/Keras** for the DL model, and **Streamlit** for the user interface.
- A detailed README in this folder explains how to set up the project, configure your database, and run the web app.


## Installation & Setup

To set up the complete repository on your local machine, follow these steps:

1. **Clone the repository:**
 
   ```bash
   git clone https://github.com/JacksonDivakar/Projects.git
    ```

2. **Create a virtual environment (recommended):**
    
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    ```
    
3. **Install the required packages:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Set up your MySQL database:**
    
    - Create the necessary tables (`user_data`, `food_nutrients`, `nutrients_data`, `user_nutrition`).
        
    - Import any initial data as needed.
        
5. **Run the Nutrition Tracker Project:**
    
    ```bash
    streamlit run Nutrition_Tracker_Project/app.py
    ```
    
6. **Explore the notebooks:**
    
    - Open the notebooks in Jupyter or any other preferred IDE to explore EDA, DL, ML, and Time Series projects.
        

## Usage

- For quick experimentation, open the notebooks under each folder and run the cells step by step.
    
- For the full application, run the Nutrition Tracker through Streamlit as mentioned above.
    

## Future Developments

- Extend the Nutrition Tracker with additional features such as user profiles, historical tracking, and nutrition recommendations.
    
- Enhance the ML and DL projects with ensemble methods and advanced deep learning architectures.
    
- Expand the Time Series analysis section with real-world forecasting projects.
    

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Contact

For any questions or suggestions, please contact Jackson Divakar (mailto:jacksondivakar@gmail.com).

---


