import customtkinter as ctk


class SelectInput(ctk.CTkToplevel):
    def __init__(self, inputs, assign_input):
        self.assign_input = assign_input

        super().__init__()

        self.geometry(f'300x400')
        self.title('Select Input')

        for input_ in inputs:
            button = ctk.CTkButton(self, text=input_,
                                   command=lambda i=input_: self.assign_input_and_close(i))
            button.pack(fill='x', pady=10, padx=10)

    def assign_input_and_close(self, i):
        self.assign_input(i)
        self.destroy()
