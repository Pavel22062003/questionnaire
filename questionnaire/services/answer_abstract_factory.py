from questionnaire.models import Block
from questionnaire.services.multiple_answer_manager import MultipleAnswerManager
from questionnaire.services.single_answer_manager import SingleAnswerManager


class AnswerAbstractFactory:
    def __init__(self, data, user, current_block, block_type: Block.Type):
        self.data = data
        self.user = user
        self.current_block = current_block
        self.__class = MultipleAnswerManager if block_type == Block.Type.SIMPLE else SingleAnswerManager
        self.__controller = None

    def process(self):
        self.__controller = self.__class(data=self.data, user=self.user, current_block=self.current_block)
        formatted_answers = self.__controller.format_answers()
        self.__controller.save_or_update_answers(formatted_answers)

    def get_next_block(self):
        return self.__controller.get_next_block()
