import toga

class Navigator:
    def __init__(self, main_window: toga.MainWindow):
        self.main_window = main_window
        self.screens = {}

    def register_screen(self, name: str, screen_factory):
        self.screens[name] = screen_factory

    def navigate(self, name: str):
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not registered")

        widget = self.screens[name](self)
        self.main_window.content = widget

