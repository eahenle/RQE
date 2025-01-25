import tkinter as tk
from tkinter import scrolledtext
from RQE import RouterQueryEngine

class FrontEnd():
    """
    FrontEnd is the user interface for the MosaicAI system.
    It provides a simple GUI chat interface for users to interact with the RQE system.

    Use `FrontEnd.run()` to start the chat interface.
    """
    def __init__(self, root=tk.Tk(), **kwargs):
        super().__init__(**kwargs)
        self.rqe = RouterQueryEngine(**kwargs)
        self.init_gui(root)
        return

    def init_gui(self, root):
        """
        Initialize the GUI components: chat area and input entry.
        """
        # set up the main window
        self.root = root
        self.root.title("Mosaic RQE")
        # set up the chat log area
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # set up the user input entry
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)
        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        # send the input on Enter key press
        self.entry.bind("<Return>", self.send_message)
        return

    def send_message(self, event=None):
        """
        On user input, add the message to the chat, query the RQE system, and display the response.
        """
        user_message = self.entry.get()
        if user_message.strip():
            self.entry.delete(0, tk.END) # clear the text field
            self.display_message("{user}", user_message) # add user message to chat
            bot_response = self.rqe.query(user_message) # query the RQE system
            self.display_message("MosaicAI", bot_response) # add bot response to chat
        return

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
        return
    
    def run(self):
        """
        Start the chat interface.
        """
        self.root.mainloop()
        return
