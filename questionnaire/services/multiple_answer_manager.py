from collections import defaultdict

from questionnaire.models import Question, Answer, UserAnswer
from questionnaire.services.abstract_answer_manager import AbstractAnswerManager
from questionnaire.services.base_answer_manager import BaseAnswerManager


class MultipleAnswerManager(AbstractAnswerManager, BaseAnswerManager):

    def process_answers(self):
        formatted_answers = self.format_answers()
        self.save_or_update_answers(formatted_answers)

    def format_answers(self):
        block_questions = self.current_block.questions.all()
        result = defaultdict(str)
        for question in block_questions:
            answer = self.data.get(str(question.uuid))
            if answer:
                result[question] = answer
        return result

    def save_or_update_answers(self, formatted_answers: defaultdict[Question, str]):
        instances_to_save = []
        instances_to_update = []
        question__uuids = [v.uuid for v in formatted_answers.keys()]
        user_answers = UserAnswer.objects.filter(question__uuid__in=question__uuids, user=self.user,
                                                 type=UserAnswer.Type.MULTIPLE)
        user_answers_dict = {el.question.uuid: el for el in user_answers}
        for question, answer in formatted_answers.items():
            instance = user_answers_dict.get(question.uuid)
            if instance:
                setattr(instance, 'user_answer', answer)
                instances_to_update.append(instance)
            else:
                instances_to_save.append(
                    UserAnswer(user=self.user, question=question, user_answer=answer, type=UserAnswer.Type.MULTIPLE))
        UserAnswer.objects.bulk_create(instances_to_save, batch_size=100)
        UserAnswer.objects.bulk_update(instances_to_update, ['user_answer'], batch_size=100)

    def get_next_block(self):
        next_block: Answer = self.current_block.answers.all().first()
        if next_block:
            return next_block.next_block
        else:
            return None
