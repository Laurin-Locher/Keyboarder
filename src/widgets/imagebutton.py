import customtkinter as ctk


class ImageButton(ctk.CTkLabel):
    def __init__(self, master, image, pressed_image, command):
        self.image = image

        super().__init__(master, image=image, text='')
        self.bind('<Button>', lambda _: self.configure(image=pressed_image))

        self.bind('<ButtonRelease>', lambda _: self.configure(image=self.image))
        self.bind('<ButtonRelease>', command)


