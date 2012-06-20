from django.contrib.gis import admin
from models import Program


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title' ]

admin.site.register(Program, ProgramAdmin)
