from django.contrib import admin
from voters.models import Voter
from voting.models import Votingpoll
# Register your models here.

admin.site.register(Voter)
admin.site.register(Votingpoll)
