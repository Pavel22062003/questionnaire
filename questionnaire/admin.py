from django.contrib import admin
from questionnaire.models import Questionnaire, Question, Answer, Block


@admin.register(Questionnaire)
class AdminTest(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Question)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['text']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['title']
