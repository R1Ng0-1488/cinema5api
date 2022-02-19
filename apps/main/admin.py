from django.contrib import admin

from .models import Movie, City, Session, Cinema


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass 


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    pass 


class SessionInline(admin.TabularInline):
    model = Session 
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (SessionInline,)