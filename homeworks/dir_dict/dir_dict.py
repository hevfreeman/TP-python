import os


class DirDict:
    def __file_path(self, filename):
        return os.path.join(self._dir_path, filename)

    def __init__(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self._dir_path = path

    def __len__(self):
        return len(os.listdir(self._dir_path))

    def __iter__(self):
        for item_filename in os.listdir(self._dir_path):
            yield item_filename
            # with open(self.__file_path(item_filename), 'r') as item_file:
            #     yield item_file.read()

    def __getitem__(self, item):
        if os.path.isfile(self.__file_path(item)):
            with open(self.__file_path(item), 'r') as item_file:
                return item_file.read()
        else:
            raise KeyError(item)

    def __setitem__(self, key, value):
        self.__delitem__(key)
        with open(self.__file_path(key), 'w') as item_file:
            item_file.write(value)

    def __delitem__(self, key):
        if os.path.isfile(self.__file_path(key)):
            os.remove(self.__file_path(key))

    def __str__(self):
        s = "{"
        for key in self:
            s += f"'{key}': '{self[key]}', "
        s = s[:-2]
        s += "}"
        return s




