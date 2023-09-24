import tkinter as tk
from tkinter import ttk, scrolledtext

class PlayerUnit(ttk.Frame):
    def __init__(self, parent, player, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.player = player

        # Frame style
        self['borderwidth'] = 2
        self['relief'] = "ridge"  # This gives a slightly raised effect
        self['padding'] = (10, 10)

        # Player's Name Label with bold font
        self.name_label = ttk.Label(self, text=self.player.name, font=("Arial", 14, "bold"))
        self.name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # Role Label
        self.role_label = ttk.Label(self, text=f"Role: {self.player.role}", font=("Arial", 12))
        self.role_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # External Dialogue ScrolledText with a title
        ttk.Label(self, text="External Dialogue", font=("Arial", 12, "italic")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.dialogue_box = scrolledtext.ScrolledText(self, width=25, height=5, wrap=tk.WORD)
        self.dialogue_box.grid(row=3, column=0, padx=5, pady=5)

        # Vote Status Label
        self.vote_status = ttk.Label(self, text="Vote: ?", font=("Arial", 12))
        self.vote_status.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        # Internal Dialogue ScrolledText (Only for Spies) with a title
        if self.player.role == 'spy':
            ttk.Label(self, text="Internal Dialogue", font=("Arial", 12, "italic")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
            self.internal_dialogue_box = scrolledtext.ScrolledText(self, width=25, height=5, wrap=tk.WORD)
            self.internal_dialogue_box.grid(row=6, column=0, padx=5, pady=5)

    def update_external_dialogue(self, text):
        self.dialogue_box.delete("1.0", tk.END) #clears it...
        self.dialogue_box.insert(tk.END, text)
        self.dialogue_box.yview(tk.END) # Auto-scroll to end

    def update_vote(self, vote):
        self.vote_status["text"] = "Vote: " + vote
