import tkinter as tk
from tkinter import PhotoImage, StringVar
from threading import Thread
from main2 import VoiceAssistant
from datetime import datetime

class VoiceAssistantUI(tk.Tk):
    def __init__(self, assistant):
        super().__init__()

        self.assistant = assistant

        self.title("Voice Assistant")
        self.geometry("800x600")

       
        image_path = "E:\python_project\jarvis\image\wp4500201-iron-man-dark-wallpapers.png"
        self.background_image = PhotoImage(file=image_path)
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

 
        calculator_buttons = [
            ('7', 0.8, 0.7), ('8', 0.85, 0.7), ('9', 0.9, 0.7),
            ('4', 0.8, 0.75), ('5', 0.85, 0.75), ('6', 0.9, 0.75),
            ('1', 0.8, 0.8), ('2', 0.85, 0.8), ('3', 0.9, 0.8),
            ('0', 0.85, 0.85), ('+', 0.95, 0.7), ('-', 0.95, 0.75),
            ('*', 0.95, 0.8), ('/', 0.95, 0.85), ('C', 0.95, 0.9),
            ('=', 0.95, 0.95)
        ]

        for button_text, relx, rely in calculator_buttons:
            button = tk.Button(self, text=button_text, command=lambda t=button_text: self.update_calculator(t),
                               font=('Helvetica', 12), bd=2, relief='raised', bg='black', fg='white')
            button.place(relx=relx, rely=rely, relwidth=0.05, relheight=0.05)


        self.calculator_var = StringVar()
        self.calculator_entry = tk.Entry(self, textvariable=self.calculator_var, font=('Helvetica', 14),
                                         justify='right', bd=2, relief='raised', bg='black', fg='white')
        self.calculator_entry.place(relx=1, rely=0.68, anchor='e', relwidth=0.2)
        self.calculator_entry.config(highlightthickness=0) 

        # Time and Date Display
        self.time_date_label = tk.Label(self, text="", font=("Helvetica", 12, 'bold'), bg='black', fg='white', bd=0)
        self.time_date_label.place(relx=0.05, rely=0.05, anchor='nw')  
        self.time_date_label.config(highlightthickness=0)  
        self.update_time_date()

        # Start Button
        self.start_button = tk.Button(self, text="Start Voice Assistant", command=self.start_assistant, bg='white', bd=2,
                                      relief='raised', borderwidth=5, font=('Helvetica', 12))
        self.start_button.place(relx=0.5, rely=0.5, anchor='center')

    def start_assistant(self):
        
        assistant_thread = Thread(target=self.assistant.run)
        assistant_thread.start()

    def update_time_date(self):
        
        current_time_date = datetime.now().strftime("%I:%M:%S %p - %d/%m/%Y")
        self.time_date_label.config(text=current_time_date)
        self.after(1000, self.update_time_date)  # Schedule the next update after 1000 milliseconds (1 second)

    def update_calculator(self, button_text):
        if button_text == '=':
            try:
                result = eval(self.calculator_var.get())
                self.calculator_var.set(str(result))
            except Exception as e:
                self.calculator_var.set("Error")
        elif button_text == 'C':
            self.calculator_var.set("")
        else:
            current_text = self.calculator_var.get()
            self.calculator_var.set(current_text + button_text)

if __name__ == "__main__":
    assistant = VoiceAssistant()

    # Create and run the UI
    ui = VoiceAssistantUI(assistant)
    assistant.wish_me()
    ui.mainloop()
