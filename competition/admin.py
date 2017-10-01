from django.contrib import admin
from .models import Competition, Rank
# Register your models here.

class RankInline(admin.TabularInline):
    model = Rank


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [
        RankInline,
    ]



admin.site.register(Competition, CompetitionAdmin)
