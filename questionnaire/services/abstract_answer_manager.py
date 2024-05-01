from abc import ABC, abstractmethod


class AbstractAnswerManager(ABC):

    @abstractmethod
    def format_answers(self):
        pass

    @abstractmethod
    def save_or_update_answers(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_next_block(self):
        pass
