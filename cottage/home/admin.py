from django.contrib import admin

from .models import CakeDisplay

class CakeDisplayAdmin(admin.ModelAdmin):
    """Category admin model class defined."""

    search_fields = ['^name']

    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'price', 'description','image' )
        }),
    )

admin.site.register(CakeDisplay, CakeDisplayAdmin)
