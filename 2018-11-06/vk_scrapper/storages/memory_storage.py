from storages.storage import Storage


class MemoryStorage(Storage):
    """Simple storage class for testing purpose."""
    def __init__(self) -> object:
        self.lines = []

    def read_data(self):
        for line in self.lines:
            yield line

    def write_data(self, data_array):
        """
        :param data_array: collection of strings that
        should be written as lines
        """
        if type(data_array) is str:
            self.lines.append(data_array)
        else:
            self.lines.extend(data_array)

    def append_data(self, data):
        """
        :param data: string
        """
        self.lines.append(data)
