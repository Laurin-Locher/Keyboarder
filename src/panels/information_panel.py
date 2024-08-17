import customtkinter as ctk
from src.widgets.imagebutton import ImageButton
from PIL import Image


class InformationPanel(ctk.CTkFrame):
    def __init__(self, master, synth, current_parameters, highlight_color, octave, window, background):
        self.synth = synth
        self.current_parameters = current_parameters
        self.highlight_color = background
        self.window = window
        self.background = background
        
        super().__init__(master)

        self.synth_title = ctk.CTkLabel(self, text=self.current_parameters.title,
                                        font=('Arial', 60))
        self.synth_title.place(relx=0.5, rely=0.01, anchor='n', relheight=0.2, relwidth=1)

        # ui_scale = ctk.DoubleVar(value=1)
        # ui_scale.trace_add('write', lambda _, __, ___: ctk.set_widget_scaling(ui_scale.get()))
        #
        # ui_scaler = ctk.CTkSlider(self, variable=ui_scale, from_=0, to=2)
        # ui_scaler.place(relx=0.95, rely=.95, relwidth=.69, anchor='se')

        self.create_graph()

    def create_graph(self):
        self.graph = ctk.CTkCanvas(self, bg='#222', highlightthickness=0)
        self.graph.place(relx=0.5, rely=0.22, relheight=0.6, relwidth=0.98, anchor='n')
        self.graph.update()
        self.bind('<Configure>', lambda _: self.draw_graph(loop=False))
        self.draw_graph()

    def draw_graph(self, loop=True):
        self.graph.delete('all')
        buffer = self.synth.get_buffer()
        width = self.graph.winfo_width()
        factor_x = width / len(buffer)
        height = self.graph.winfo_height()
        x0 = y0 = None
        for i in range(len(buffer)):
            x1 = int(i * factor_x)
            y1 = int(.5 * height + .45 * height * buffer[i])
            if x0 is not None:
                self.graph.create_line(x0, y0, x1, y1, fill='white')
            x0 = x1
            y0 = y1

        if loop:
            self.after(10, self.draw_graph)
    