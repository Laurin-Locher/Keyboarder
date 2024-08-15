import customtkinter as ctk
from src.widgets.imagebutton import ImageButton
from PIL import Image


class InformationPanel(ctk.CTkFrame):
    def __init__(self, master, synth, current_parameters, highlight_color, octave, window):
        self.synth = synth
        self.current_parameters = current_parameters
        self.highlight_color = highlight_color
        self.octave = octave
        self.window = window
        
        super().__init__(master)

        self.synth_title = ctk.CTkLabel(self, text=self.current_parameters.title,
                                        font=('Arial', 60))
        self.synth_title.place(relx=0.5, rely=0.01, anchor='n', relheight=0.2, relwidth=1)
        octave_changer = self.create_octave_changer()

        padding = 0.01
        octave_changer.place(relx=0 + padding, rely=1 - padding, anchor='sw', relwidth=0.3, relheight=.1)

        ui_scale = ctk.DoubleVar(value=1)
        ui_scale.trace_add('write', lambda _, __, ___: ctk.set_widget_scaling(ui_scale.get()))

        ui_scaler = ctk.CTkSlider(self, variable=ui_scale, from_=0, to=2)
        ui_scaler.place(relx=0.95, rely=.95, relwidth=.69, anchor='se')

        self.create_graph()

    def create_graph(self):
        self.graph = ctk.CTkCanvas(self, bg='#444', highlightthickness=0)
        self.graph.place(relx=0.5, rely=0.22, relheight=0.6, relwidth=0.98, anchor='n')
        self.graph.update()
        self.draw_graph()

    def draw_graph(self):
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
        self.after(10, self.draw_graph)
        
    def create_octave_changer(self):
        octave_frame = ctk.CTkFrame(self, fg_color=self.highlight_color)
        self.octave_label = ctk.CTkLabel(octave_frame, text=f'octave: {self.octave}', font=('Arial', 20))

        change_frame = ctk.CTkFrame(octave_frame, fg_color=self.highlight_color)
        increase = self.create_image_button(change_frame, 'increase', lambda _: self.synth.change_octave(1))
        decrease = self.create_image_button(change_frame, 'decrease', lambda _: self.synth.change_octave(-1))

        increase.pack()
        decrease.pack()
        change_frame.pack(side='left', padx=10)
        self.octave_label.pack(side='left', padx=10)

        self.window.bind('<KeyPress-Up>', lambda _: self.synth.change_octave(1))
        self.window.bind('<KeyPress-Down>', lambda _: self.synth.change_octave(-1))

        return octave_frame

    @staticmethod
    def create_image_button(master, folder, command):
        white_normal = Image.open(f'resource/symbols/{folder}/white/normal.png')
        white_pressed = Image.open(f'resource/symbols/{folder}/white/pressed.png')
        black_normal = Image.open(f'resource/symbols/{folder}/black/normal.png')
        black_pressed = Image.open(f'resource/symbols/{folder}/black/pressed.png')
        normal = ctk.CTkImage(light_image=black_normal,
                              dark_image=white_normal
                              )
        pressed = ctk.CTkImage(light_image=black_pressed,
                               dark_image=white_pressed
                               )
        increase = ImageButton(master, normal, pressed, command)
        return increase


    