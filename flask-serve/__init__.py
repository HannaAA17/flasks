from io import BytesIO


class ExcelFile:
    def __init__(self):
        self._file = self.open()

    @property
    def file(self):
        self._file.seek(0)
        return self._file

    def open(self):
        with open("./draweez.xlsx", "rb") as f:
            buf = BytesIO(f.read())
        return buf
