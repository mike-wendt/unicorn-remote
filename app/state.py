import multiprocessing
import unicornhat
import importlib
import sys
import os

import app.config


class State:
    ''' Handles the Unicorn HAT state'''

    def __init__(self):
        self._process = None

    def start_program(self, name, params={}):
        try:
            program = app.config.programs[name]
        except KeyError:
            raise KeyError("Program '{}' was not found".format(name))

        self.stop_program()

        if "brightness" in params:
            unicornhat.brightness(float(params["brightness"]))

        if "rotation" in params:
            unicornhat.rotation(int(params["rotation"]))

        program = importlib.import_module(program["module"])
        self._process = multiprocessing.Process(target=program.run, args=(params,))
        self._process.start()

    def stop_program(self):
        if self._process is not None:
            self._process.terminate()
        unicornhat.show()


state = State()