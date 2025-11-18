from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import DoctorForm
from .models import *

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split


# ---------- Public Views ----------

def Home(request):
    return render(request, 'carousel.html')

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Gallery(request):
    return render(request, 'gallery.html')


# ---------- Authentication ----------

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            if Patient.objects.filter(user=user).exists():
                login(request, user)
                error = "pat1"
            elif Doctor.objects.filter(user=user, status=1).exists():
                login(request, user)
                error = "pat2"
            else:
                error = "notmember"
        else:
            error = "not"
    return render(request, 'login.html', {'error': error})

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user and user.is_staff:
            login(request, user)
            error = "pat"
        else:
            error = "notmember" if user else "not"
    return render(request, 'admin_login.html', {'error': error})

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        if User.objects.filter(username=u).exists():
            error = "exists"
        else:
            user = User.objects.create_user(
                username=u,
                password=request.POST['pwd'],
                first_name=request.POST['fname'],
                last_name=request.POST['lname'],
                email=request.POST['email']
            )
            im = request.FILES.get('image')
            d = request.POST['dob']
            if request.POST['type'] == "Patient":
                Patient.objects.create(user=user, contact=request.POST['contact'], address=request.POST['add'], image=im, dob=d)
            else:
                Doctor.objects.create(user=user, contact=request.POST['contact'], address=request.POST['add'], image=im, dob=d, status=2)
            error = "create"
    return render(request, 'register.html', {'error': error})

def Logout(request):
    logout(request)
    return redirect('home')


# ---------- Home Pages ----------

@login_required(login_url="login")
def Admin_Home(request):
    d = {
        'dis': Search_Data.objects.count(),
        'pat': Patient.objects.count(),
        'doc': Doctor.objects.count(),
        'feed': Feedback.objects.count()
    }
    return render(request, 'admin_home.html', d)

@login_required(login_url="login")
def User_Home(request):
    return render(request, 'patient_home.html')

@login_required(login_url="login")
def Doctor_Home(request):
    return render(request, 'doctor_home.html')


# ---------- Doctor Management ----------

@login_required(login_url="login")
def assign_status(request, pid):
    doctor = Doctor.objects.get(id=pid)
    doctor.status = 2 if doctor.status == 1 else 1
    doctor.save()
    messages.success(request, 'Doctor status updated.')
    return redirect('view_doctor')

@login_required(login_url="login")
def View_Doctor(request):
    return render(request, 'view_doctor.html', {'doc': Doctor.objects.all()})

@login_required(login_url="login")
def delete_doctor(request, pid):
    Doctor.objects.get(id=pid).delete()
    return redirect('view_doctor')

@login_required(login_url="login")
def add_doctor(request, pid=None):
    doctor = Doctor.objects.get(id=pid) if pid else None
    error = ""
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            new_doc = form.save(commit=False)
            new_doc.status = 1
            if not pid:
                username = request.POST['username']
                if User.objects.filter(username=username).exists():
                    error = "exists"
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=request.POST['password'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email']
                    )
                    new_doc.user = user
                    new_doc.save()
                    return redirect('view_doctor')
            else:
                new_doc.save()
                return redirect('view_doctor')
    return render(request, 'add_doctor.html', {'doctor': doctor, 'error': error})


# ---------- Patient Management ----------

@login_required(login_url="login")
def View_Patient(request):
    return render(request, 'view_patient.html', {'patient': Patient.objects.all()})

@login_required(login_url="login")
def delete_patient(request, pid):
    Patient.objects.get(id=pid).delete()
    return redirect('view_patient')


# ---------- Feedback ----------

@login_required(login_url="login")
def View_Feedback(request):
    return render(request, 'view_feedback.html', {'dis': Feedback.objects.all()})

@login_required(login_url="login")
def delete_feedback(request, pid):
    Feedback.objects.get(id=pid).delete()
    return redirect('view_feedback')

@login_required(login_url="login")
def sent_feedback(request):
    terror = None
    if request.method == "POST":
        Feedback.objects.create(
            user=User.objects.get(username=request.POST['uname']),
            messages=request.POST['msg']
        )
        terror = "create"
    return render(request, 'sent_feedback.html', {'terror': terror})


# ---------- Heart Disease Prediction ----------

def prdict_heart_disease(list_data):
    csv_file = Admin_Helath_CSV.objects.get(id=1)
    df = pd.read_csv(csv_file.csv_file)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    model.fit(X_train, y_train)
    pred = model.predict([list_data])
    accuracy = model.score(X_test, y_test) * 100

    # get prediction probability
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([list_data])[0]
        prob_healthy = float(proba[0] * 100)
        prob_disease = float(proba[1] * 100)
    else:
        prob_disease = 100.0 if pred[0] == 1 else 0.0
        prob_healthy = 100.0 - prob_disease

    return round(accuracy, 2), pred, round(prob_healthy, 2), round(prob_disease, 2)


@login_required(login_url="login")
def add_heartdetail(request):
    if request.method == "POST":
        post_data = dict(request.POST.lists())
        list_data = []
        for k, v in post_data.items():
            if k != 'csrfmiddlewaretoken':
                value = v[0].strip().lower()
                if k == 'sex':
                    list_data.append(0 if value.startswith("m") else 1)
                else:
                    list_data.append(float(v[0]))
        accuracy, pred, prob_healthy, prob_disease = prdict_heart_disease(list_data)
        patient = Patient.objects.get(user=request.user)
        # ✅ Save probabilities in Search_Data
        Search_Data.objects.create(
            patient=patient,
            prediction_accuracy=accuracy,
            result=pred[0],
            values_list=list_data,
            prob_healthy=prob_healthy,
            prob_disease=prob_disease
        )
        return redirect(
            f"/predict_desease/{int(pred[0])}/{accuracy}/?prob_healthy={prob_healthy}&prob_disease={prob_disease}"
        )
    return render(request, 'add_heartdetail.html')


@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    prob_healthy = float(request.GET.get("prob_healthy", 0))
    prob_disease = float(request.GET.get("prob_disease", 0))

    # choose highest probability
    if prob_healthy >= prob_disease:
        probability_label = "Healthy"
        probability_value = prob_healthy
    else:
        probability_label = "Heart Disease"
        probability_value = prob_disease

    pat = Patient.objects.get(user=request.user)
    doctor = Doctor.objects.filter(address__icontains=pat.address)
    result_text = "✅ You are healthy." if int(pred) == 0 else "⚠️ You may have heart disease."

    return render(request, 'predict_disease.html', {
        'pred': pred,
        'accuracy': accuracy,
        'doctor': doctor,
        'prob_healthy': prob_healthy,       # keep both for graph
        'prob_disease': prob_disease,       # keep both for graph
        'probability_label': probability_label,  # highest label
        'probability_value': probability_value,  # highest value
        'result_text': result_text
    })


# ---------- Search & Logs ----------

@login_required(login_url="login")
def view_search_pat(request):
    try:
        doc = Doctor.objects.get(user=request.user)
        data = Search_Data.objects.filter(patient__address__icontains=doc.address).order_by('-id')
    except Doctor.DoesNotExist:
        try:
            pat = Patient.objects.get(user=request.user)
            data = Search_Data.objects.filter(patient=pat).order_by('-id')
        except Patient.DoesNotExist:
            data = Search_Data.objects.all().order_by('-id')
    return render(request, 'view_search_pat.html', {'data': data})

@login_required(login_url="login")
def delete_searched(request, pid):
    Search_Data.objects.get(id=pid).delete()
    return redirect('view_search_pat')


# ---------- Profiles ----------

@login_required(login_url="login")
def View_My_Detail(request):
    user = request.user
    try:
        profile = Patient.objects.get(user=user)
        error = "pat"
    except Patient.DoesNotExist:
        profile = Doctor.objects.get(user=user)
        error = ""
    return render(request, 'profile_doctor.html', {'error': error, 'pro': profile})

@login_required(login_url="login")
def Edit_Doctor(request, pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        doc.user.first_name = request.POST['fname']
        doc.user.last_name = request.POST['lname']
        doc.user.email = request.POST['email']
        doc.contact = request.POST['contact']
        doc.category = request.POST['type']
        doc.address = request.POST['add']
        if 'image' in request.FILES:
            doc.image = request.FILES['image']
        doc.user.save()
        doc.save()
        error = "create"
    return render(request, 'edit_doctor.html', {'error': error, 'doc': doc})

@login_required(login_url="login")
def Edit_My_deatail(request):
    user = request.user
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except Patient.DoesNotExist:
        sign = Doctor.objects.get(user=user)
        error = ""
    if request.method == 'POST':
        sign.user.first_name = request.POST['fname']
        sign.user.last_name = request.POST['lname']
        sign.user.email = request.POST['email']
        sign.contact = request.POST['contact']
        sign.address = request.POST['add']
        if 'image' in request.FILES:
            sign.image = request.FILES['image']
        if error != "pat":
            sign.category = request.POST['type']
        sign.user.save()
        sign.save()
        return render(request, 'edit_profile.html', {'error': error, 'terror': "create", 'doc': sign})
    return render(request, 'edit_profile.html', {'error': error, 'doc': sign})


# ---------- Password Change ----------

@login_required
def Change_Password(request):
    user = request.user
    terror = ""

    if request.method == "POST":
        old_password = request.POST.get("pwd3")
        new_password = request.POST.get("pwd1")
        confirm_password = request.POST.get("pwd2")

        if not user.check_password(old_password):
            terror = "wrong"
        elif new_password != confirm_password:
            terror = "not"
        else:
            user.set_password(new_password)
            user.save()
            terror = "yes"

    try:
        sign = Patient.objects.get(user=user)
        user_type = "patient"
    except Patient.DoesNotExist:
        try:
            sign = Doctor.objects.get(user=user)
            user_type = "doctor"
        except Doctor.DoesNotExist:
            sign = None
            user_type = "admin"

    return render(request, "change_password.html", {"terror": terror, "sign": sign, "user_type": user_type})
