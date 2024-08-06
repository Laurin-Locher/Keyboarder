import customtkinter as ctk


class Key(ctk.CTkFrame):
    def __init__(self, master, key_type: str, sound, keyboardVisualizer):
        self.keyboardVisualizer = keyboardVisualizer

        self.colors: (str, str, str)
        if key_type == 'white':
            self.colors = ('#fff', '#aaa', '#777', '#000')
            self.border_width = 5
        elif key_type == 'black':
            self.colors = ('#000', '#333', '#444')
            self.border_width = 0

        self.normal_color = self.colors[0]
        self.hover_color = self.colors[1]
        self.press_color = self.colors[2]

        super().__init__(master, fg_color=self.normal_color, border_width=self.border_width, border_color='#000')
        self.is_hovering = False

        self.bind('<Enter>', self.hover)
        self.bind('<Leave>', self.leave)

        self.bind('<Button>', self.key_down)
        self.bind('<ButtonRelease>', self.key_up)

        self.sound = sound

    def hover(self, _):
        self.is_hovering = True
        self.configure(fg_color=self.hover_color)

    def leave(self, _):
        self.is_hovering = False
        self.configure(fg_color=self.normal_color)

    def key_down(self, _, call_visualizer=True):
        if call_visualizer:
            self.keyboardVisualizer.key_down(self.sound)
        self.configure(fg_color=self.press_color)

    def key_up(self, _, call_visualizer=True):
        if call_visualizer:
            self.keyboardVisualizer.key_up(self.sound)

        if self.is_hovering:
            self.configure(fg_color=self.hover_color)

        else:
            self.configure(fg_color=self.normal_color)
