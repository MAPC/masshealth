from models import Hero
from django.contrib import admin


class HeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'active','rank', ]
    list_editable = ['active', 'rank']

admin.site.register(Hero,HeroAdmin)
