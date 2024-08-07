
class KeyboardVisualizer:

    def key_down(self, note: (str, int), update_gui: bool):
        raise NotImplemented

    def key_up(self, note: (str, int)):
        raise NotImplemented
