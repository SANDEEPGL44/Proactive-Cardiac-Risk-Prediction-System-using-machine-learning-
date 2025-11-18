❤️ Proactive Cardiac Risk Prediction System Using Machine Learning

A full-stack web application that proactively predicts the risk of cardiac (heart) disease using trained Machine Learning models.
This system helps patients, doctors, and administrators access predictions, manage records, and analyze health data using an interactive Django-based interface.

🚀 Project Overview

The Proactive Cardiac Risk Prediction System predicts whether a person is at high risk of developing heart disease based on clinical attributes.
It integrates a machine learning model, deployed inside a Django web framework, with three user roles:

Admin

Doctor

Patient

The system is designed for clinical analysis, healthcare decision support, and academic demonstration.

⭐ Key Features
🔐 Authentication & Roles

Secure Login & Signup

Admin / Doctor / Patient access levels

Profile management

🧑‍💼 Patient Module

Enter health attributes

View prediction results

See prediction history

Edit personal profile

Submit feedback

👨‍⚕️ Doctor Module

Access patient health records

Analyze prediction outcomes

Provide medical remarks

Edit profile

🛠️ Admin Module

Manage doctors

Manage patients

View all predictions

Manage feedback

Control model/dataset updates

🤖 Machine Learning Integration

Cleaned and preprocessed dataset

Trained classification models

Model saved as .pkl

Real-time prediction execution

🧠 Machine Learning Details
🧪 Algorithms Used

Multiple ML models were trained and evaluated:

--> Logistic Regression

--> Gradient Boosting

The best-performing model was deployed based on:

Accuracy

Precision

Recall

F1-score

Confusion Matrix

📌 Final Deployed Model File
ml_model/cardiac_risk_model.pkl

🩺 Input Features

Age

Sex

Chest Pain Type

Resting Blood Pressure

Serum Cholesterol

Fasting Blood Sugar

Rest ECG

Max Heart Rate

Exercise Induced Angina

ST Depression (Oldpeak)

Slope

Major Vessels (0–3)

Thalassemia (0–3)

🛠 Tech Stack
Frontend

HTML5

CSS3

Bootstrap

JavaScript

Backend

Python

Django

SQLite / MySQL

ML Libraries

scikit-learn

numpy

pandas

📂 Project Structure
ProactiveCardiacRiskPrediction/
│── core/
│── accounts/
│── doctor/
│── patient/
│── prediction/
│── ml_model/
│── static/
│── templates/
│── manage.py
│── requirements.txt

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate   # Linux/Mac

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py migrate

5️⃣ Start the Server
python manage.py runserver

6️⃣ Visit the App
http://127.0.0.1:8000/

🔑 Default Admin Login
Username: admin
Password: admin123

🖼 Screenshots

(Add your screenshots under /images/)

![Home](images/home.png)
![Prediction Form](images/predict.png)
![Dashboard](images/dashboard.png)

🔮 Future Enhancements

Deep Learning-based cardiac prediction

PDF report export

REST API for mobile app

IoT device integration for live vitals

Email/SMS alerts for high-risk cases

📄 License

This project is licensed under the MIT License.

👨‍💻 Author

Sandeep G L
Machine Learning Engineer | Python & Django Developer
GitHub: github.com/SANDEEPGL44
LinkedIn: linkedin.com/in/sandeep-g-l-98a903231
