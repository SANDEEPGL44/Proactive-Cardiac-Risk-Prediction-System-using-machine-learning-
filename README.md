🫀 Proactive Cardiac Risk Prediction System Using Machine Learning

A Machine Learning–based web application designed to predict heart disease risk using clinical parameters.
This project aims to assist early diagnosis by providing a prediction model integrated into a user-friendly interface.

🚀 Features

✔ Machine Learning Model for predicting heart disease risk

✔ Django Web Application with clean UI

✔ Admin, Doctor & Patient Roles

✔ User Authentication – Login, Signup

✔ Patient Dashboard with prediction history

✔ Doctor Dashboard to view patient records

✔ Feedback System

✔ Mobile-friendly UI

📁 Project Structure
Heart-Disease-Prediction-System-main/
│── dataset/                 # CSV data for ML training
│── model/                   # Trained ML model (pickle)
│── static/                  # CSS, JS, Images
│── templates/               # HTML Templates
│── heart/                   # Main Django App
│── manage.py                # Django project runner
└── requirements.txt         # Dependencies

🧠 Machine Learning Model

The model is trained using the Heart Disease UCI dataset.
Algorithms used:

Logistic Regression

Gradient Boosting

Random Forest

SVM

KNN

Final model selected based on highest accuracy.

Input Features Include:

Age

Sex

Chest Pain Type

Resting BP

Cholesterol

Fasting Blood Sugar

Resting ECG

Maximum Heart Rate

Exercise-Induced Angina

Oldpeak (ST Depression)

Slope

Major Vessels

Thalassemia

🛠 Tech Stack

Frontend: HTML, CSS, Bootstrap
Backend: Django
ML: Python, scikit-learn, NumPy, Pandas
Database: SQLite / MySQL

▶ How to Run the Project
1. Clone the Repository
git clone https://github.com/your-username/Heart-Disease-Prediction-System-main.git
cd Heart-Disease-Prediction-System-main

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

3. Install Requirements
pip install -r requirements.txt

4. Run Migrations
python manage.py migrate

5. Run Server
python manage.py runserver

6. Open in Browser
http://127.0.0.1:8000/

🔐 Default Admin Credentials (If Applicable)
Username: admin
Password: admin123

📊 Model Accuracy

Add your accuracy results here, e.g.:

Logistic Regression: 84%

Gradient Boosting: 90%

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue to discuss your idea.

📜 License

This project is licensed under the MIT License.
