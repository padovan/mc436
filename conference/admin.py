from django.contrib import admin
from conference.models import *

class AreaAdmin(admin.ModelAdmin):
    list_display = ('area', 'description', )
    search_fields = ['area']
    ordering = ['area']

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email', )
    search_fields = ['username', 'last_name', 'first_name', 'email']
    ordering = ['username', 'last_name', 'first_name']

class SponsorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount','max_invites' ,)
    search_fields = ['name']
    ordering = ['name', 'amount']

class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_invited', )

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email',)
    search_fields = ['username', 'last_name', 'first_name', 'email']
    ordering = ['username' 'last_name, first_name']

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email',)
    search_fields = ['username', 'last_name', 'first_name', 'email']
    ordering = ['username' 'last_name, first_name']

class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email', 'status',)
    search_fields = ['username', 'last_name', 'first_name', 'email']
    ordering = ['username', 'status']
    list_filter = ['status']

class TextAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    ordering = ['title']


admin.site.register(Area, AreaAdmin)
admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(SponsorType, SponsorTypeAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Participant, SiteUserAdmin)
admin.site.register(Speaker, SiteUserAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Text, TextAdmin)


