import importlib
import os
from _should import Should


class StepRunner(object):
    def __init__(self, reporter):
        self.reporter = reporter

    def load_steps(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for f in files:
                if f.endswith('test.py') or \
                        f.endswith('tests.py') or \
                        f.startswith('test'):
                    # TODO: magic to get the name and stuff right
                    importlib.import_module(f)

        self.reporter.aggregate()


class ConsoleReporter(object):
    # TODO: report each step's success/failure/error
    # TODO: report final stats
    # TODO: verbosity...

    def aggregate(self):
        pass


class StepCounter(object):
    # TODO: must preserve context of step (given, when, then, etc...)
    # TODO: timing of steps and entire suite

    def __init__(self, reporter):
        self.reporter = reporter

    def start(self, step, name):
        pass

    def finish(self, name):
        pass

    def error(self, name, exception_type, exception, traceback):
        pass

    def fail(self, name, exception_type, exception, traceback):
        pass


class Step(object):
    def __init__(self, step, counter):
        self._step = step
        self._counter = counter
        self._name = None

    @property
    def name(self):
        return '{0} {1}'\
            .format(self._step, self._name)\
            .replace('_', ' ')\
            .strip()

    def __getattr__(self, item):
        if self._name is not None:
            raise AttributeError('You may only specify a single name.')

        self._name = item
        return self

    def __enter__(self):
        self._counter.start(self._step, self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._counter.finish(self.name)

        elif isinstance(exc_val, AssertionError):
            self._counter.fail(self.name, exc_type, exc_val, exc_tb)

        elif isinstance(exc_val, KeyboardInterrupt):
            return False

        else:
            self._counter.error(self.name, exc_type, exc_val, exc_tb)

        return True


reporter = ConsoleReporter()
runner = StepRunner(reporter)
counter = StepCounter(reporter)

given = Step('given', counter)
when = Step('when', counter)
and_ = Step('and', counter)
then = Step('then', counter)

the = Should
it = Should
this = Should


# TODO: this goes in a script installed in the path
if __name__ == '__main__':
    runner.load_steps()