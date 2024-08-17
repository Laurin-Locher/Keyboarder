import customtkinter as ctk


# from src.app import App


class Selector(ctk.CTkFrame):
    def __init__(self, master, background, app):
        self.background = background
        self.app = app

        super().__init__(master, fg_color=background, border_color='#555', border_width=2)

        self.synthesizer_names: list = [
            "Hans Wurst",
            "Berta Brezel",
            "Frieda Frosch",
            "Max Mustermann",
            "Lena Lämpchen",
            "Sigi Sorglos",
            "Otto Normalverbraucher",
            "Uwe Umweg",
            "Franz Futteral",
            "Greta Gurke"
        ]
        self.synthesizer_frames = []
        self.last_index = 0
        self.current_index = 0

    def update_selector(self):
        self.clean_up()
        self.create_elements()
        self.update_selection()

    def clean_up(self):
        for widget in self.synthesizer_frames:
            widget.pack_forget()

        self.synthesizer_frames = []

    def create_elements(self):
        for index, synth in enumerate(self.app.all_parameters):
            frame = ctk.CTkFrame(self, fg_color=self.background)

            text = ctk.CTkLabel(frame, text=f'{index + 1}: {synth.title}', justify='left', font=('Arial', 25))
            text.pack(fill='x', side='left', pady=5, padx=5)

            frame.pack(fill='x', padx=10, pady=10)

            self.synthesizer_frames.append(frame)

            frame.bind('<Button>', lambda _, i=index: self.set_synth(i))
            text.bind('<Button>', lambda _, i=index: self.set_synth(i))

    def set_synth(self, index):
        self.last_index = self.current_index
        self.current_index = index

        self.update_selection()

        self.app.set_current_bank(self.current_index)

    def update_selection(self):
        from src.app import ACCENT_COLOR
        self.synthesizer_frames[self.last_index].configure(border_width=0)
        self.synthesizer_frames[self.current_index].configure(border_width=2, border_color=ACCENT_COLOR)

