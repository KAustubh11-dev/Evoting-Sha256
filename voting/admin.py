from django.contrib import admin
from voting.models import Administration, Result, Voted
# Register your models here.

admin.site.register(Administration)
admin.site.register(Result)
admin.site.register(Voted)
