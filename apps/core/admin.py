from django.contrib import admin

from .models import GrammarLesson, Vocabulary


@admin.register(GrammarLesson)
class GrammarLessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_fix.css',)
        }

    list_display = ('title', 'topic')


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ('word_number', 'word_name', 'part_of_speech', 'hindi_meaning', 'created_at')
    list_filter = ('part_of_speech',)
    search_fields = ('word_name', 'hindi_meaning', 'definition')
    ordering = ('word_number',)
    readonly_fields = ('created_at',)
