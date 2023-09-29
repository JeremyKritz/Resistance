import tkinter as tk
from tkinter import ttk, scrolledtext

class PlayerUnit(ttk.Frame):
    def __init__(self, parent, player, *args, **kwargs):
        # Create a style
        self.style = ttk.Style()

        if player.role == 'spy':
            self.style.configure('Spy.TFrame', background='lightcoral')
            super().__init__(parent, style='Spy.TFrame', *args, **kwargs)
        else:
            self.style.configure('Resistance.TFrame', background='lightblue')
            super().__init__(parent, style='Resistance.TFrame', *args, **kwargs)

        self.player = player

        # Frame style
        self['borderwidth'] = 2
        self['relief'] = "ridge"
        self['padding'] = (10, 10)

        # Player's Name Label with bold font
        self.name_label = ttk.Label(self, text=self.player.name, font=("Arial", 14, "bold"))
        self.name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # Role Label
        self.role_label = ttk.Label(self, text=f"Role: {self.player.role}", font=("Arial", 12))
        self.role_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # External Dialogue ScrolledText with a title
        ttk.Label(self, text="External Dialogue", font=("Arial", 12, "italic")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.dialogue_box = scrolledtext.ScrolledText(self, width=30, height=10, wrap=tk.WORD)
        self.dialogue_box.grid(row=3, column=0, padx=5, pady=5)

        # Vote Status Label
        self.vote_status = ttk.Label(self, text="Vote: ?", font=("Arial", 12))
        self.vote_status.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        # Vote Canvas for visualization
        self.vote_canvas = tk.Canvas(self, width=20, height=20)
        self.vote_canvas.grid(row=1, column=1)
        self.vote_square = self.vote_canvas.create_rectangle(2, 2, 18, 18, fill="white") # default white, updated later


        # Internal Dialogue ScrolledText (Only for Spies) with a title
        if self.player.role == 'spy':
            ttk.Label(self, text="Internal Dialogue", font=("Arial", 12, "italic")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
            self.internal_dialogue_box = scrolledtext.ScrolledText(self, width=30, height=10, wrap=tk.WORD)  # Reduce width
            self.internal_dialogue_box.grid(row=6, column=0, padx=5, pady=5)


    def update_dialogue(self, dialogue_box, text):
        dialogue_box.delete("1.0", tk.END)  # clears it...

        words = text.split()
        for word in words:
            dialogue_box.insert(tk.END, word + " ")
            dialogue_box.yview(tk.END)  # Auto-scroll to end
            dialogue_box.update_idletasks()  # Force an update of the GUI
            dialogue_box.after(90) 

    def update_external_dialogue(self, text):
        self.update_dialogue(self.dialogue_box, text)

    def update_internal_dialogue(self, text):
        self.update_dialogue(self.internal_dialogue_box, text)


    def update_vote(self, vote):
        if vote == "pass":
            color = "blue"
        elif vote == "fail":
            color = "red"
        else:
            color = "white"
        self.vote_canvas.itemconfig(self.vote_square, fill=color)
        self.vote_status["text"] = "Vote: " + vote

    def clear_all(self):
        # Clear the external dialogue
        self.dialogue_box.delete("1.0", tk.END)

        # Clear the internal dialogue if player is a spy
        if hasattr(self, 'internal_dialogue_box'):
            self.internal_dialogue_box.delete("1.0", tk.END)
        
        # Reset the vote
        self.vote_status["text"] = "Vote: ?"
        self.vote_canvas.itemconfig(self.vote_square, fill="white")