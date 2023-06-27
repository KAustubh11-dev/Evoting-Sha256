from django.urls import path, include
from candidates import views

urlpatterns = [
    path("candidateregistration", views.CandidateRegistration.as_view(),
         name="candidateregistration"),
    path("candidatelogin", views.CandidateLogin.as_view(), name="candidatelogin"),
    path("candidatelogout", views.CandidateLogout, name="candidatelogout"),
]
