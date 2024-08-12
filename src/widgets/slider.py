import customtkinter as ctk


class Slider(ctk.CTkCanvas):
    def __init__(self, master, variable=None, from_=0, to=1, slider_width=10, canvas_bg='#000', bg_color='#333',
                 fg_color='#fff', orientation='vertical', has_handle=False, handle_width=20, handle_height=8,
                 handle_color='#fff'):

        if orientation == 'vertical' or orientation == 'v':
            self._orientation = 0

        elif orientation == 'horizontal' or orientation == 'h':
            self._orientation = 1

        self._from_ = from_
        self._to = to
        self._slider_width = slider_width
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._has_handle = has_handle
        self._handle_width = handle_width
        self._handle_height = handle_height
        self._handle_color = handle_color

        if variable:
            self._variable = variable
        else:
            self._variable = ctk.DoubleVar(value=.6)

        self._variable.trace_add('write', self._update_value_from_variable)

        super().__init__(master, bg=canvas_bg, relief='flat', borderwidth=0, highlightthickness=0)

        self.can_update_from_variable = True

        self._update_value_from_variable()

        self.bind('<Configure>', self.redraw)

        self.is_pressed = False
        self.bind('<Button>', self._on_button_down)
        self.bind('<ButtonRelease>', self._on_button_release)
        self.bind('<Motion>', self._on_mouse_motion)

    def redraw(self, _, redraw_everything=True):
        if redraw_everything:
            self.delete('all')
        else:
            self.delete('value')

        height = self.winfo_height()
        width = self.winfo_width()

        if self._orientation == 0:
            self.x1 = width / 2 - self._slider_width / 2
            self.y1 = 0

            self.x2 = width / 2 + self._slider_width / 2
            self.y2 = height

        elif self._orientation == 1:
            self.x1 = 0
            self.y1 = height / 2 - self._slider_width / 2

            self.x2 = width
            self.y2 = height / 2 + self._slider_width / 2

        if redraw_everything:
            self.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self._bg_color, outline=self._bg_color)

        if self._orientation == 0:
            self.y1 = height - height * self.value

        elif self._orientation == 1:
            self.x2 = self.x1
            self.x1 = width - width * self.value

        self.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self._fg_color, outline=self._fg_color, tags='value')

        if self._has_handle:
            if self._orientation == 0:
                self.hx1 = width / 2 - self._handle_width / 2
                self.hy1 = self.y1 + self._handle_height / 2

                self.hx2 = self.hx1 + self._handle_width
                self.hy2 = self.hy1 - self._handle_height

            elif self._orientation == 1:
                self.hx1 = self.x1 - self._handle_height / 2
                self.hy1 = height / 2 + self._handle_width / 2

                self.hx2 = self.hx1 + self._handle_height
                self.hy2 = self.hy1 - self._handle_width

            self.create_rectangle(self.hx1, self.hy1, self.hx2, self.hy2, fill=self._handle_color,
                                  outline=self._handle_color, tags='value')

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
            if self._orientation == 0:
                self.new_value = 1 - event.y / self.winfo_height()
            elif self._orientation == 1:
                self.new_value = 1 - event.x / self.winfo_width()

            self.value = (min(1.0, max(0.0, self.new_value)))

        except ZeroDivisionError:
            self.value = 0

        self._update_variable()

        self.redraw(None, False)

    def _update_variable(self):
        self.can_update_from_variable = False
        if self._orientation == 0:
            self._variable.set(self._from_ + (self._to - self._from_) * self.value)
        elif self._orientation == 1:
            self._variable.set(self._from_ + (self._to - self._from_) * (1 - self.value))

        self.can_update_from_variable = True

    def _update_value_from_variable(self, *args):
        if self.can_update_from_variable:
            new_value: float = (self._variable.get() - self._from_) / (self._to - self._from_)

            self.value = (min(1.0, max(0.0, new_value)))

            self.redraw(None, False)


# window = ctk.CTk()
# window.geometry('100x400')
#
# Slider(window, has_handle=True, orientation='h').pack(expand=True, fill='both', pady=10)
#
# window.mainloop()
