
from django.contrib import admin
from .models import SavedGrammar, SavedVocabulary, UserWordDefinitions, UserVocabulary, UserSavedContent, UserFreeTierStart, UserDailyStoryUsage, UserDailyMessageUsage, UserDailyDoubtSolving
from django.core.exceptions import ValidationError

@admin.register(SavedGrammar)
class SavedGrammarAdmin(admin.ModelAdmin):
    list_display = ('user', 'simple_sentence', 'tense', 'modal_part_1', 'modal_part_2', 'causative_verb', 'voice', 'other')
    list_filter = ('simple_sentence', 'tense', 'modal_part_1', 'modal_part_2', 'causative_verb', 'voice', 'other')
    search_fields = ('user__email',)
    raw_id_fields = ('user',)  # Helps with performance if many users exist
    list_editable = ('simple_sentence', 'tense', 'modal_part_1', 'modal_part_2', 'causative_verb', 'voice', 'other')  # Allows editing directly from list view




@admin.register(SavedVocabulary)
class SavedVocabularyAdmin(admin.ModelAdmin):
    list_display = ('user', 'word_count')
    search_fields = ('user__email', 'words')
    readonly_fields = ('word_count',)

    def word_count(self, obj):
        return len(obj.words) if obj.words else 0
    word_count.short_description = 'Words Learned'



@admin.register(UserWordDefinitions)
class UserWordDefinitionsAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'total_words', 'sample_definition')
    readonly_fields = ('user_email',)
    search_fields = ('user__email',)

    def save_model(self, request, obj, form, change):
        # Validate each definition has max 5 lines
        for word, definition in obj.definitions.items():
            line_count = len(definition.split('\n'))
            if line_count > 5:
                raise ValidationError(
                    f"Definition for '{word}' has {line_count} lines. Max allowed is 5."
                )
        super().save_model(request, obj, form, change)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def total_words(self, obj):
        return len(obj.definitions)
    total_words.short_description = 'Total Words'

    def sample_definition(self, obj):
        if obj.definitions:
            # Just show first word and part of its definition
            first_word = next(iter(obj.definitions))
            definition = obj.definitions[first_word]
            return f"{first_word}: {definition[:40]}{'...' if len(definition) > 40 else ''}"
        return "-"
    sample_definition.short_description = 'Sample Definition'




@admin.register(UserVocabulary)
class UserVocabularyAdmin(admin.ModelAdmin):
    list_display = ('user', 'word_name')
    search_fields = ('word_name', 'user__email')
    ordering = ('user',)

@admin.register(UserSavedContent)
class UserSavedContentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)
    ordering = ('user',)





@admin.register(UserFreeTierStart)
class UserFreeTierStartAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date')
    search_fields = ('user__email',)


@admin.register(UserDailyStoryUsage)
class UserDailyStoryUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'count')
    list_filter = ('date',)
    search_fields = ('user__email',)


@admin.register(UserDailyMessageUsage)
class UserDailyMessageUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'message_count')
    list_filter = ('date',)
    search_fields = ('user__email',)


@admin.register(UserDailyDoubtSolving)
class UserDailyDoubtSolvingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'message_count')
    list_filter = ('date',)
    search_fields = ('user__email',)