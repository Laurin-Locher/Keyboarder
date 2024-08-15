import customtkinter as ctk
from src.widgets.round_slider import RoundSlider

window = ctk.CTk(fg_color='green')
window.geometry('500x500')

window.columnconfigure((0, 1), weight=1, uniform='a')
window.rowconfigure((0, 1), weight=1, uniform='a')

frame = ctk.CTkFrame(window, fg_color='orange')
frame.grid(row=0, column=0, sticky='nswe')
frame.columnconfigure((0, 1), weight=1, uniform='a')
frame.rowconfigure((0, 1), weight=1, uniform='a')

frame_2 = ctk.CTkFrame(frame, fg_color='purple')
frame_2.grid(row=0, column=0, sticky='nswe')
frame_2.columnconfigure((0, 1), weight=1, uniform='a')
frame_2.rowconfigure((0, 1), weight=1, uniform='a')

frame_3 = ctk.CTkFrame(frame_2, fg_color='orange')
frame_3.grid(row=0, column=0, sticky='nswe')
frame_3.columnconfigure((0, 1), weight=1, uniform='a')
frame_3.rowconfigure((0, 1), weight=1, uniform='a')

frame_4 = ctk.CTkFrame(frame_3, fg_color='pink')
frame_4.grid(row=0, column=0, sticky='nswe')
frame_4.columnconfigure((0, 1), weight=1, uniform='a')
frame_4.rowconfigure((0, 1), weight=1, uniform='a')

slider = RoundSlider(frame_4)
slider.grid(row=0, column=0, sticky='nswe')

slider = RoundSlider(frame_4)
slider.grid(row=1, column=0, sticky='nswe')

slider = RoundSlider(frame_4)
slider.grid(row=0, column=1, sticky='nswe')


window.mainloop()
