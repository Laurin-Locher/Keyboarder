import customtkinter as ctk
from src.widgets.slider import Slider


class OvertoneControls(ctk.CTkFrame):
    def __init__(self, master, background, set_weight):
        self.set_weight = set_weight
        self.background = background

        super().__init__(master, fg_color=self.background)

        self.rowconfigure(0, weight=1)

        number_of_controls = 15

        self.columnconfigure(list(range(number_of_controls)), weight=1, uniform='a')
        self.rowconfigure(1, weight=10)

        bar = ctk.CTkFrame(self, fg_color=self.background)
        label = ctk.CTkLabel(bar, text='Overtones', font=('Arial', 15))
        label.pack(side='top', padx=10)

        def reset():
            value = 1
            for weight_ in self.overtones:
                weight_.set(value=value)
                value = 0

        reset = ctk.CTkButton(bar, text='Reset', fg_color=self.background,
                              hover_color=self.background,
                              command=reset)
        reset.pack(side='right', padx=10)
        bar.grid(row=0, column=0, columnspan=number_of_controls, pady=5)

        self.overtones = []
        default = 1

        for index in range(number_of_controls):
            weight = ctk.DoubleVar(value=default)

            from src.app import ACCENT_COLOR
            slider = Slider(self, orientation='vertical', variable=weight, slider_width=4, fg_color=ACCENT_COLOR)
            slider.grid(column=index, row=1, sticky='nswe')

            self.overtones.append(weight)

            weight.trace_add('write', callback=lambda _, __, ___, i=index, w=weight: self.set_weight(i, w))

            default = 0
