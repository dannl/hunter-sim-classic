from char.char_state import CharState
from engine import Engine
from rotation.rotation import Rotation


class Char:

    def __init__(self, engine, rotation,char_state):
        """

        :param Engine engine:
        :param Rotation rotation:
        :param CharState char_state:
        """
        self.engine = engine
        self.char_state = char_state
        self.rotation = rotation
        self.target_armor = 3750
