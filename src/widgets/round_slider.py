import customtkinter as ctk
import math


class RoundSlider(ctk.CTkCanvas):
    CUT_OUT = 60

    def __init__(self, master, from_=0, to=1, variable=None,
                 pad_in=5,
                 canvas_bg_color='#000',
                 bg_color='#333',
                 fg_color='#fff',
                 highlight_color='#777'):

        self._from_ = from_
        self._to = to
        self._value = variable
        self._pad_in = pad_in
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._highlight_color = highlight_color

        super().__init__(master, bg=canvas_bg_color, relief='flat', borderwidth=0, highlightthickness=0)

        self._value = 0
        self._can_update_value_from_variable = True

        if variable:
            self._variable = variable
        else:
            self._variable = ctk.DoubleVar(value=0)

        self._variable.trace_add('write', self._update_value_from_variable)

        self.redraw(...)

        self.bind('<Configure>', self.redraw)

        self.button_pressed = False
        self.bind('<Button>', self._on_button_press)
        self.bind('<ButtonRelease>', self._on_button_release)
        self.bind('<Motion>', lambda event: self._on_mouse_motion(event))

    def _on_button_press(self, event):
        self.button_pressed = True
        self.last_y = event.y

    def _on_button_release(self, _):
        self.button_pressed = False

    def _on_mouse_motion(self, event):
        if self.button_pressed:
            # x = event.x
            y = event.y

            # a = self.last_press_pos[0] - x
            # b = self.last_press_pos[1] - y
            # new_value = self.value + math.sqrt(a*a + b*b) / 200

            distance = self.last_y - y
            offset = distance / 200

            new_value = self._value + offset

            if new_value > 1:
                new_value = 1

            elif new_value < 0:
                new_value = 0

            self._set_value(new_value)

            self.last_y = y

    def _set_value(self, new_value):
        self._value = new_value

        self._can_update_value_from_variable = False
        self._variable.set(self._from_ + (self._to - self._from_) * self._value)
        self._can_update_value_from_variable = True

        self.redraw_line()

    def _update_value_from_variable(self, *args):
        if self._can_update_value_from_variable:
            new_value: float = (self._variable.get() - self._from_) / (self._to - self._from_)

            self.value = (min(1.0, max(0.0, new_value)))

            self.redraw_line()

    def redraw(self, _):
        self.delete('all')
        height = self.winfo_height()
        width = self.winfo_width()

        if height < width:
            self.first_pos = (width / 2 - height / 2, 0)
            self.second_pos = (self.first_pos[0] + height, self.first_pos[1] + height)

        else:
            self.first_pos = (0, height / 2 - width / 2)
            self.second_pos = (self.first_pos[0] + width, self.first_pos[1] + width)

        self._create_highlight(self.first_pos, self.second_pos)

        self.pad_from_highlight = 5
        self._create_background(self.first_pos, self.second_pos, self.pad_from_highlight)

        self.redraw_line()

    def redraw_line(self):
        self.delete('line')

        radius = (self.second_pos[0] - self.first_pos[0]) / 2
        center = (self.first_pos[0] + radius, self.first_pos[1] + radius)

        x1, y1 = self._calculate_line_endpos(self._value, center[0], center[1], radius - self.pad_from_highlight - 10)
        x2, y2 = center

        self.create_line((x1, y1, x2, y2), fill=self._fg_color, width=3, tags='line')

    def _create_background(self, first_pos, second_pos, pad_from_highlight):
        padding = self._pad_in + pad_from_highlight
        padded_pos = ((first_pos[0] + padding, first_pos[1] + padding),
                      (second_pos[0] - padding, second_pos[1] - padding))
        self.create_oval(padded_pos, fill=self._bg_color, outline=self._bg_color)

    def _create_highlight(self, first_pos, second_pos):
        padding = self._pad_in + 1
        padded_pos = ((first_pos[0] + padding, first_pos[1] + padding),
                      (second_pos[0] - padding, second_pos[1] - padding))

        self.create_arc(padded_pos, fill=self._highlight_color, outline=self._highlight_color,
                        start=270 + self.CUT_OUT / 2,
                        extent=360 - self.CUT_OUT)

    def _calculate_line_endpos(self, value, x_center, y_center, radius):
        min_angle = 90 + self.CUT_OUT / 2
        max_angle = 360 + self.CUT_OUT

        # Angle to 'Bogenmass'
        angle_min_rad = math.radians(min_angle)
        angle_max_rad = math.radians(max_angle)

        # angle based on value
        angle = angle_min_rad + value * (angle_max_rad - angle_min_rad)

        # calculate x and y
        x = x_center + radius * math.cos(angle)
        y = y_center + radius * math.sin(angle)

        return x, y


# window = ctk.CTk()
# window.rowconfigure((0, 1), weight=1, uniform='a')
# window.columnconfigure((0, 1), weight=1, uniform='a')
#
# RoundSlider(window).grid(row=0, column=0, sticky='nswe')
# RoundSlider(window).grid(row=1, column=1, sticky='nswe')
# RoundSlider(window).grid(row=0, column=1, sticky='nswe')
# RoundSlider(window).grid(row=1, column=0, sticky='nswe')
#
# window.mainloop()
