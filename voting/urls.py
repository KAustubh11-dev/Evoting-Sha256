from django.urls import path, include
from voting import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("adminlogin", views.AdminLogin.as_view(), name="adminlogin"),
    path("adminlogout", views.AdminLogout, name="adminlogout"),
    path("createvotingpoll", views.CreateVotingPoll.as_view(),
         name="createvotingpoll"),
    path("voting", views.VotePoll.as_view(), name="voting"),
    path("resultlist", views.VotingResultList.as_view(), name="votinglist"),
]
