from questionnaire.models import Answer, UserAnswer
from questionnaire.services.abstract_answer_manager import AbstractAnswerManager
from questionnaire.services.base_answer_manager import BaseAnswerManager


class SingleAnswerManager(AbstractAnswerManager, BaseAnswerManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer = None

    def format_answers(self):
        answer = Answer.objects.filter(uuid__in=self.data).first()
        self.answer = answer
        return answer

    def save_or_update_answers(self, formatted_answer):
        user_answer = UserAnswer.objects.filter(user=self.user, answer__current_block=self.current_block,
                                                type=UserAnswer.Type.CHECKBOX).first()
        if user_answer:
            setattr(user_answer, 'answer', formatted_answer)
            setattr(user_answer, 'user_answer', formatted_answer.answer)
            user_answer.save()
        else:
            UserAnswer.objects.create(user=self.user, answer=formatted_answer,
                                      user_answer=formatted_answer.answer, type=UserAnswer.Type.CHECKBOX)

    def get_next_block(self):
        return self.answer.next_block
