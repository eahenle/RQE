import tkinter as tk
from tkinter import scrolledtext
from Agent import Agent

class FrontEnd(Agent):
    def __init__(self, root=tk.Tk(), **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.root.title("Mosaic RQE")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)

        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message.strip():
            self.display_message("You", user_message)
            bot_response = self.get_bot_response(user_message)
            self.display_message("Bot", bot_response)
        self.entry.delete(0, tk.END)

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def get_bot_response(self, message):
        return self.query(message, self.system_message)
    
    def run(self):
        self.root.mainloop()
        return None
