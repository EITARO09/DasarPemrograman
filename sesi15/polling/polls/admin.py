from django.contrib import admin
from .models import Poll, Choice, Vote

class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')  # <-- Tampilkan ID dan pertanyaan

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
