from django.urls import path, include
from voters import views

urlpatterns = [
    path("voterregistration", views.VoterRegistration.as_view(),
         name="voterregistration"),
    path("voterlogin", views.VoterLogin.as_view(), name="voterlogin"),
    path("voterlogout", views.VoterLogout, name="voterlogout"),
    path("voting", views.VotePoll.as_view(), name="voting"),
]
