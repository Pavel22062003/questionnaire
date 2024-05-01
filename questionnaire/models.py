from config.models import BaseModel
from django.db import models


class Questionnaire(BaseModel):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='questionnaires/', null=True)


class Block(BaseModel):
    class Type(models.TextChoices):
        COMPLICATE = 'complicate'
        SIMPLE = 'simple'

    title = models.CharField(max_length=100)
    type = models.CharField(choices=Type.choices, max_length=255)
    is_first_block = models.BooleanField(default=False)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(BaseModel):
    text = models.CharField(max_length=100)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, related_name='questions')

    def __str__(self):
        return self.text


class Answer(BaseModel):
    current_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100, null=True, blank=True)
    next_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='previous_block')

    def __str__(self):
        return self.answer if self.answer else f'Связка для блока {self.current_block} и {self.next_block}'


class UserAnswer(BaseModel):
    class Type(models.TextChoices):
        CHECKBOX = 'checkbox'
        MULTIPLE = 'multiple'

    type = models.CharField(choices=Type.choices, max_length=255)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_answers', null=True)
    user_answer = models.TextField()
