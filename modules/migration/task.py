import enum
from enum import IntEnum
from xml.etree.ElementTree import Element


class TaskState(IntEnum):
    NEW = 0,
    DONE = 1,
    REPETITION = 2,
    ERROR = 3


class Task(object):
    def __init__(self, element: Element, max_repetition_count=10):
        self.__element__ = element
        self.__max_repetition_count__ = max_repetition_count
        self.__status__ = TaskState.NEW

        self.set_repetition(0)

    def get_repetition(self) -> int:
        return int(self.__get_attribute__('repetition', 0))

    def get_errors(self) -> int:
        return int(self.__get_attribute__('errors', 0))

    def get_source_path(self) -> str:
        return self.__element__[0].text

    def get_source_size(self) -> int:
        return int(self.__get_attribute__('size', 0, self.__element__[0]))

    def get_target_path(self) -> str:
        return self.__element__[1].text

    def get_target_size(self) -> int:
        return int(self.__get_attribute__('size', 0, self.__element__[1]))

    def get_completeness(self) -> float:
        completeness = self.__get_attribute__('completeness', 0)
        if completeness != 0:
            completeness = completeness.replace('%', '')
        return float(completeness)

    def set_errors(self, value: int):
        self.__set_attribute('errors', value)

    def set_target_size(self, value: int):
        repetition = self.get_repetition()
        if value == self.get_target_size():
            repetition += 1
        else:
            repetition = 0

        self.__set_attribute('repetition', repetition)
        completeness = '{:.2%}'.format(value / self.get_source_size())
        self.__set_attribute('completeness', completeness)
        self.__set_attribute('size', value, self.__element__[1])

    def set_repetition(self, value: int):
        self.__set_attribute('repetition', value)

    def get_status(self) -> TaskState:
        if self.get_completeness() == 100:
            self.__status__ = TaskState.DONE
        elif self.get_repetition() >= self.__max_repetition_count__:
            self.__status__ = TaskState.REPETITION
            self.set_errors(self.get_errors() + 1)

        return self.__status__

    def set_status(self, value: TaskState):
        self.__status__ = value
        if value == TaskState.DONE:
            self.__set_attribute('completeness', '100.00%')
            self.__set_attribute('size', self.get_source_size(), self.__element__[1])
            self.set_errors(0)
        if value == TaskState.ERROR:
            self.set_errors(self.get_errors() + 1)

    def __get_attribute__(self, attribute_name, default_value: any, element=None) -> any:
        if element is None:
            element = self.__element__

        attribute = element.get(attribute_name)
        if attribute:
            return attribute
        else:
            return default_value

    def __set_attribute(self, attribute_name, value: any, element=None):
        if element is None:
            element = self.__element__

        element.set(attribute_name, str(value))
