import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Event
import time

class PlayerUnit(ttk.Frame):
    def __init__(self, parent, player, *args, **kwargs):
        # Create a style
        self.style = ttk.Style()
        self.dialogue_finished_event = Event()

        if player.role == 'spy':
            self.style.configure('Spy.TFrame', background='lightcoral')
            super().__init__(parent, style='Spy.TFrame', *args, **kwargs)
        else:
            self.style.configure('Resistance.TFrame', background='lightblue')
            super().__init__(parent, style='Resistance.TFrame', *args, **kwargs)

        self.player = player
        self.updating_external = False

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
        self.dialogue_box = scrolledtext.ScrolledText(self, width=30, height=14, wrap=tk.WORD)
        self.dialogue_box.grid(row=3, column=0, padx=5, pady=5)

        # Vote Status Label
        self.vote_status = ttk.Label(self, text="Vote: ?", font=("Arial", 12))
        self.vote_status.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        # Vote Canvas for visualization
        self.vote_canvas = tk.Canvas(self, width=20, height=20)
        self.vote_canvas.grid(row=1, column=1)
        self.vote_square = self.vote_canvas.create_rectangle(2, 2, 18, 18, fill="white") # default white, updated later


        # Internal Dialogue ScrolledText (Only for Spies) with a title

        ttk.Label(self, text="Internal Dialogue", font=("Arial", 12, "italic")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.internal_dialogue_box = scrolledtext.ScrolledText(self, width=30, height=14, wrap=tk.WORD)  # Reduce width
        self.internal_dialogue_box.grid(row=6, column=0, padx=5, pady=5)


    def insert_word(self, dialogue_box, words, index=0, callback=None):
        if index < len(words):
            dialogue_box.insert(tk.END, words[index] + " ")
            dialogue_box.yview(tk.END)  # Auto-scroll to the latest inserted word
            dialogue_box.after(90, self.insert_word, dialogue_box, words, index+1, callback) #ms
        else:
            self.unhighlight_talking()
            
            if callback:
                callback()

    def update_dialogue_box(self, dialogue_box, text, callback=None):
        """Updates the provided dialogue_box with the given text.""" 
        # Clear the dialogue box
        dialogue_box.delete("1.0", tk.END)  
        self.highlight_talking()
        words = text.split()
        self.insert_word(dialogue_box, words, callback=callback)

    def update_dialogue(self, external_text=None, internal_text=None):     
        def after_internal_update():
            """Callback function to update external dialogue after internal."""
            if external_text:
                self.update_dialogue_box(self.dialogue_box, external_text)
                
        if internal_text:
            self.update_dialogue_box(self.internal_dialogue_box, internal_text, callback=after_internal_update)
        elif external_text:
            self.update_dialogue_box(self.dialogue_box, external_text)



    def update_vote(self, vote):
        if vote == "pass":
            color = "blue"
        elif vote == "fail":
            color = "red"
        else:
            color = "white"
        self.vote_canvas.itemconfig(self.vote_square, fill=color)
        self.vote_status["text"] = "Vote: " + vote

    def highlight_talking(self):
        """ Highlight the player frame when they're talking """
        if self.player.role == 'spy':
            self.style.configure('Spy.TFrame', bordercolor='yellow')
        else:
            self.style.configure('Resistance.TFrame', bordercolor='yellow')

    def unhighlight_talking(self):
        """ Remove the highlight from the player frame """
        if self.player.role == 'spy':
            self.style.configure('Spy.TFrame', bordercolor='lightcoral')
        else:
            self.style.configure('Resistance.TFrame', bordercolor='lightblue')

    def clear_all(self):
        # Clear the external dialogue
        self.dialogue_box.delete("1.0", tk.END)

        # Clear the internal dialogue if player is a spy
        if hasattr(self, 'internal_dialogue_box'):
            self.internal_dialogue_box.delete("1.0", tk.END)
        
        # Reset the vote
        self.vote_status["text"] = "Vote: ?"
        self.vote_canvas.itemconfig(self.vote_square, fill="white")