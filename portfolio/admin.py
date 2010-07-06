from django.contrib import admin
from portfolio.models import Solution

class SolutionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Solution, SolutionAdmin)