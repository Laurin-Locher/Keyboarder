import customtkinter as ctk


class Slider(ctk.CTkCanvas):
    def __init__(self, master, variable=None, from_=0, to=1, slider_width=10, canvas_bg='#000', bg_color='#333',
                 fg_color='#fff', orientation='vertical'):
        self._from_ = from_
        self._to = to
        self._slider_width = slider_width
        self._bg_color = bg_color
        self._fg_color = fg_color

        if variable:
            self.variable = variable

        else:
            self.variable = ctk.DoubleVar(value=0)

        self.variable.trace_add('write', self._update_value_from_variable)

        super().__init__(master, bg=canvas_bg)

        self.value = self.variable.get()

        self.bind('<Configure>', self.redraw)

        self.is_pressed = False
        self.bind('<Button>', self._on_button_down)
        self.bind('<ButtonRelease>', self._on_button_release)
        self.bind('<Motion>', self._on_mouse_motion)

        self._update_value_from_variable()

    def redraw(self, _, redraw_everything=True):
        if redraw_everything:
            self.delete('all')
        else:
            self.delete('value')

        height = self.winfo_height()
        width = self.winfo_width()

        x1 = width / 2 - self._slider_width / 2
        y1 = 0

        x2 = width / 2 + self._slider_width / 2
        y2 = height

        if redraw_everything:
            self.create_rectangle(x1, y1, x2, y2, fill=self._bg_color, outline=self._bg_color)

        y3 = height - height * self.value

        self.create_rectangle(x1, y3, x2, y2, fill=self._fg_color, outline=self._fg_color, tags='value')

    def _on_button_down(self, event):
        self.is_pressed = True

        self._update_value(event)

    def _on_button_release(self, _):
        self.is_pressed = False

    def _on_mouse_motion(self, event):
        if self.is_pressed:
            self._update_value(event)

    def _update_value(self, event):
        try:
            self.value = 1 - event.y / self.winfo_height()
        except ZeroDivisionError:
            self.value = 0

        self._update_variable()

        self.redraw(None, False)

    def _update_variable(self):
        self.variable.set(self._from_ + (self._to - self._from_) * self.value)

    def _update_value_from_variable(self, *args):
        new_value: float = self.variable.get() - self._from_ / (self._to - self._from_)

        self.value = (min(1.0, max(0.0, new_value)))

        self.redraw(None, False)


# window = ctk.CTk()
# window.geometry('100x400')
#
# Slider(window).pack(expand=True, fill='both', pady=10)
#
# window.mainloop()
