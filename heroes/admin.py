from models import Hero
from django.contrib import admin

class HeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'active','rank', ]
    list_editable = ['active', 'rank']

class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )

admin.site.register(Hero,HeroAdmin,
    Media = Commonmedia,
    )
