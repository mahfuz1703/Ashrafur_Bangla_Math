from django.contrib import admin
from .models import ProblemSolution, Category, ProblemStatus, UserProfile

# Register your models here.
admin.site.register(ProblemSolution)
admin.site.register(Category)
admin.site.register(ProblemStatus)
admin.site.register(UserProfile)
