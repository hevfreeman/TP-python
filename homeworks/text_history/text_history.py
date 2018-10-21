
from abc import ABC, abstractmethod
from copy import deepcopy

from my_itertools import pairwise


class TextHistory:
    def __init__(self):
        self.__text = ''
        self.__version = 0
        self.__actions_history = {}  # keys are .from_version of stored values

    @property
    def text(self):
        return self.__text

    @property
    def version(self):
        return self.__version

    def action(self, action):
        if self.__version > action.to_version:
            raise ValueError('current TextHistory version is higher that to_version')
        self.__actions_history[self.__version] = action
        self.__version = action.to_version
        self.__text = action.apply(self.__text)
        return action.to_version

    def insert(self, text, pos=None):
        return self.action(InsertAction(pos=pos if pos is not None else len(self.__text),
                           text=text,
                           from_version=self.__version,
                           to_version=self.__version+1))

    def replace(self, text, pos=None):
        return self.action(ReplaceAction(text=text,
                           pos=pos if pos is not None else len(self.__text),
                           from_version=self.__version,
                           to_version=self.__version + 1))

    def delete(self, pos, length):
        return self.action(DeleteAction(pos,
                                        length=length,
                                        from_version=self.__version,
                                        to_version=self.__version + 1))

    @staticmethod
    def _optimize_actions__merge(action_list):
        optimized_action_list = action_list.copy()
        for action1, action2 in pairwise(action_list):
            try:
                action2.merge_previous(action1)
                optimized_action_list.remove(action1)
            except ValueError:
                pass
        return optimized_action_list

    def get_actions(self, from_version=0, to_version=None, optimize=False):
        if to_version is None:
            to_version = self.__version
        if not (0 <= from_version <= to_version <= self.version):
            raise ValueError('versions error')

        keys = [k for k in self.__actions_history.keys() if from_version <= k < to_version]
        values = [self.__actions_history[k] for k in keys]

        if optimize:
            copy_values = deepcopy(values)  # not to change initial actions list
            values = TextHistory._optimize_actions__merge(copy_values)
        return values


class Action(ABC):
    def __init__(self, pos, from_version, to_version):
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version

    @abstractmethod
    def apply(self, text):
        if self.from_version >= self.to_version:
            raise ValueError('from_version >= to_version')
        if self.pos is not None and (self.pos > len(text) or self.pos < 0):
            raise ValueError('wrong pos')

    @abstractmethod
    def merge_previous(self, previous_action):
        if type(self) != type(previous_action):
            raise ValueError(f'unable to merge {type(previous_action)} with {type(self)}')
        if not (previous_action.from_version < previous_action.to_version <= self.from_version < self.to_version):
            raise ValueError('versions error')


class InsertAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        super().__init__(pos, from_version, to_version)
        self.text = text

    def apply(self, text):
        super().apply(text)
        return text[:self.pos] + self.text + text[self.pos:]

    def merge_previous(self, previous_action):
        super().merge_previous(previous_action)
        if previous_action.pos == self.pos:  # left
            self.text += previous_action.text
        elif self.pos == previous_action.pos + len(previous_action.text):  # right
            self.pos = previous_action.pos
            self.text = previous_action.text + self.text
        else:
            return 'unable to merge actions with given positions'
        self.from_version = previous_action.from_version


class ReplaceAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        super().__init__(pos, from_version, to_version)
        self.text = text

    def apply(self, text):
        super().apply(text)
        return text[:self.pos] + self.text + text[self.pos+len(self.text):]

    def merge_previous(self, previous_action):
        super().merge_previous(previous_action)
        if self.pos + len(self.text) == previous_action.pos:  # left
            self.text += previous_action.text
        elif previous_action.pos + len(previous_action.text) == self.pos:  # right
            self.text = previous_action.text + self.text
            self.pos = previous_action.pos
        else:
            raise ValueError('unable to merge actions with given positions')
        self.from_version = previous_action.from_version


class DeleteAction(Action):
    def __init__(self, pos, length, from_version, to_version):
        super().__init__(pos, from_version, to_version)
        self.length = length

    def apply(self, text):
        super().apply(text)
        if len(text) < self.pos + self.length:
            raise ValueError('wrong length')
        return text[:self.pos] + text[self.pos+self.length:]

    def merge_previous(self, previous_action):
        super().merge_previous(previous_action)

        if self.pos + self.length == previous_action.pos:  # left
            pass
        elif self.pos == previous_action.pos:  # right
            self.pos = previous_action.pos
        else:
            raise ValueError('unable to merge actions with given positions')
        self.length += previous_action.length
        self.from_version = previous_action.from_version
