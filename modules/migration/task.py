from enum import IntEnum
from xml.etree.ElementTree import Element


class TaskState(IntEnum):
    NEW = 0,
    DONE = 1,
    REPETITION = 2,
    ERROR = 3


class Task(object):
    def __init__(self, element: Element, max_repetition_count=20):
        self.__element__ = element
        self.__max_repetition_count__ = max_repetition_count
        self.__status__ = TaskState.NEW

        self.repetition = 0

    @property
    def repetition(self) -> int:
        return int(self.__get_attribute__('repetition', 0))

    @repetition.setter
    def repetition(self, value):
        self.__set_attribute('repetition', value)

    @property
    def errors(self) -> int:
        return int(self.__get_attribute__('errors', 0))

    @errors.setter
    def errors(self, value: int):
        self.__set_attribute('errors', value)

    @property
    def source_path(self) -> str:
        return self.__element__[0].text

    @property
    def source_size(self) -> int:
        return int(self.__get_attribute__('size', 0, self.__element__[0]))

    @property
    def target_path(self) -> str:
        return self.__element__[1].text

    @property
    def target_size(self) -> int:
        return int(self.__get_attribute__('size', 0, self.__element__[1]))

    @property
    def completeness(self) -> float:
        completeness = self.__get_attribute__('completeness', 0)
        if completeness != 0:
            completeness = completeness.replace('%', '')
        return float(completeness)

    @target_size.setter
    def target_size(self, value: int):
        repetition = self.repetition
        if value == self.target_size:
            repetition += 1
        else:
            repetition = 0

        self.__set_attribute('repetition', repetition)
        completeness = '{:.2%}'.format(value / self.source_size)
        self.__set_attribute('completeness', completeness)
        self.__set_attribute('size', value, self.__element__[1])

    @property
    def status(self) -> TaskState:
        if self.completeness == 100:
            self.__status__ = TaskState.DONE
        elif self.repetition >= self.__max_repetition_count__:
            self.__status__ = TaskState.REPETITION
            self.errors += 1
        return self.__status__

    @status.setter
    def status(self, value: TaskState):
        self.__status__ = value
        if value == TaskState.DONE:
            self.__set_attribute('completeness', '100.00%')
            # self.__set_attribute('size', self.get_source_size(), self.__element__[1])
            self.errors = 0
        if value == TaskState.ERROR:
            self.errors += 1

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
