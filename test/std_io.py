import io
import sys


def stubbed_output():
    return __StubbedOutput()


class __StubbedOutput:
    def __enter__(self):
        self.std_output = sys.stdout
        sys.stdout = _LinesStringIO()
        return self.lines

    def lines(self, newline: str = '\n'):
        if newline is None:
            return self._lines()
        return [line for line in self._lines() if line != newline]

    def _lines(self):
        return self.stored_lines if hasattr(self, 'stored_lines') else sys.stdout.lines

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stored_lines = sys.stdout.lines  # This line here, and the if above is only, so one can use the returned lambda outside of with/as block
        sys.stdout = self.std_output


class _LinesStringIO(io.StringIO):
    def __init__(self):
        super().__init__()
        self.lines = []

    def write(self, s: str) -> int:
        self.lines.append(s)
        return super().write(s)
