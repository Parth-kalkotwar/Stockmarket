from django.contrib import admin
from .models import Company, News


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Company, CompanyAdmin)
admin.site.register(News)
