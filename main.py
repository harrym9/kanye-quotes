from tkinter import *
import requests
from PIL import Image, ImageTk
import random
import threading
import time
import os
from datetime import datetime

class KanyeQuotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanye Says...")
        self.root.config(padx=40, pady=40, bg="#121212")
        self.root.minsize(500, 600)
        
        if os.path.exists("kanye.png"):
            icon = PhotoImage(file="kanye.png")
            self.root.iconphoto(False, icon)
        
        self.quotes_history = []
        self.current_quote_index = -1
        self.favorite_quotes = []
        
        self.setup_ui()
        
        self.kanye_says()
    
    def setup_ui(self):
        main_frame = Frame(self.root, bg="#121212")
        main_frame.pack(fill=BOTH, expand=True)
        
        title_label = Label(main_frame, 
                           text="KANYE WISDOM", 
                           font=("Helvetica", 24, "bold"), 
                           fg="#FFD700", 
                           bg="#121212")
        title_label.pack(pady=(0, 20))
        
        self.canvas = Canvas(main_frame, height=300, width=450, 
                            bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        try:
            self.bg_image = Image.open("background.png")
            self.bg_image = self.bg_image.resize((450, 300), Image.LANCZOS)
            self.photo_bg = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(225, 150, image=self.photo_bg)
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.canvas.create_rectangle(0, 0, 450, 300, fill="#1E1E1E", outline="")
            
        self.quote_text = self.canvas.create_text(
            225, 150,
            text="Welcome to Kanye Says.\nClick the button for wisdom",
            font=("Arial", 18, "bold"),
            fill="white",
            width=350,
            justify=CENTER
        )
        
        self.status_var = StringVar()
        self.status_var.set("Ready")
        status_label = Label(main_frame, textvariable=self.status_var, 
                            fg="#AAAAAA", bg="#121212", font=("Arial", 10))
        status_label.pack(pady=(5, 15))
        
        button_frame = Frame(main_frame, bg="#121212")
        button_frame.pack(pady=10)
        
        try:
            self.kanye_image = Image.open("kanye.png")
            self.kanye_image = self.kanye_image.resize((100, 100), Image.LANCZOS)
            self.photo_kanye = ImageTk.PhotoImage(self.kanye_image)
            kanye_button = Button(
                button_frame, 
                image=self.photo_kanye, 
                command=self.kanye_says,
                bg="#121212", 
                activebackground="#1E1E1E",
                highlightthickness=0, 
                borderwidth=0
            )
        except Exception as e:
            print(f"Could not load Kanye image: {e}")
            kanye_button = Button(
                button_frame, 
                text="NEW QUOTE", 
                command=self.kanye_says,
                font=("Arial", 14, "bold"),
                bg="#121212", 
                fg="#FFD700",
                padx=20, 
                pady=10
            )
        
        kanye_button.grid(row=0, column=1, padx=10)
        
        prev_button = Button(
            button_frame, 
            text="<", 
            command=self.previous_quote,
            font=("Arial", 16, "bold"),
            bg="#121212", 
            fg="#FFD700",
            padx=15, 
            pady=5
        )
        prev_button.grid(row=0, column=0, padx=10)
        
        next_button = Button(
            button_frame, 
            text=">", 
            command=self.next_quote,
            font=("Arial", 16, "bold"),
            bg="#121212", 
            fg="#FFD700",
            padx=15, 
            pady=5
        )
        next_button.grid(row=0, column=2, padx=10)
        
        self.fav_button = Button(
            button_frame, 
            text="♡", 
            command=self.toggle_favorite,
            font=("Arial", 16, "bold"),
            bg="#121212", 
            fg="#FF69B4",
            padx=15, 
            pady=5
        )
        self.fav_button.grid(row=0, column=3, padx=10)
        
        action_frame = Frame(main_frame, bg="#121212")
        action_frame.pack(pady=(20, 10), fill=X)
        
        save_button = Button(
            action_frame, 
            text="Save to File", 
            command=self.save_quote,
            font=("Arial", 12),
            bg="#333333", 
            fg="white",
            padx=10, 
            pady=5
        )
        save_button.pack(side=LEFT, padx=10)
        
        favorites_button = Button(
            action_frame, 
            text="Show Favorites", 
            command=self.show_favorites,
            font=("Arial", 12),
            bg="#333333", 
            fg="white",
            padx=10, 
            pady=5
        )
        favorites_button.pack(side=RIGHT, padx=10)
        
        self.time_var = StringVar()
        self.update_time()
        time_label = Label(main_frame, textvariable=self.time_var, 
                          fg="#AAAAAA", bg="#121212", font=("Arial", 10))
        time_label.pack(pady=(10, 0))
        
        time_thread = threading.Thread(target=self.time_updater)
        time_thread.daemon = True
        time_thread.start()
    
    def kanye_says(self):
        self.status_var.set("Fetching quote...")
        self.root.update()
        
        self.start_loading_animation()
        
        fetch_thread = threading.Thread(target=self._fetch_quote)
        fetch_thread.daemon = True
        fetch_thread.start()
    
    def _fetch_quote(self):
        try:
            response = requests.get("https://api.kanye.rest", timeout=10)
            response.raise_for_status()
            quote = response.json()["quote"]
            
            self.quotes_history.append(quote)
            self.current_quote_index = len(self.quotes_history) - 1
            
            self.root.after(0, self._update_quote_display, quote)
            self.root.after(0, self.status_var.set, "Quote loaded successfully")
            
            self.root.after(0, self._update_favorite_button)
            
        except requests.exceptions.RequestException as e:
            self.root.after(0, self.status_var.set, f"Error: {str(e)}")
            self.root.after(0, self._stop_loading_animation)
            
            backup_quotes = [
                "I am the greatest artist of all time.",
                "My greatest pain in life is that I will never be able to see myself perform live.",
                "I feel like I'm too busy writing history to read it.",
                "Everything I'm not made me everything I am.",
                "For me, money is not my definition of success. Inspiring people is a definition of success."
            ]
            backup_quote = random.choice(backup_quotes)
            self.quotes_history.append(f"[OFFLINE] {backup_quote}")
            self.current_quote_index = len(self.quotes_history) - 1
            self.root.after(0, self._update_quote_display, f"[OFFLINE] {backup_quote}")
    
    def _update_quote_display(self, quote):
        self._stop_loading_animation()
        
        self._fade_text(0)
        
        self.root.after(500, lambda: [
            self.canvas.itemconfig(self.quote_text, text=quote),
            self._fade_text(1)
        ])
    
    def _fade_text(self, direction, current=0):
        """Fade text in or out
        direction: 0 for out, 1 for in
        current: current step in the animation"""
        steps = 10
        
        if direction == 0:  # Fade out
            opacity = 1 - (current / steps)
        else:  
            opacity = current / steps
        
        color_val = int(opacity * 255)
        color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
        
        self.canvas.itemconfig(self.quote_text, fill=color)
        
        if (direction == 0 and current < steps) or (direction == 1 and current < steps):
            self.root.after(30, self._fade_text, direction, current + 1)
    
    def start_loading_animation(self):
        self.loading = True
        self.loading_dots = 0
        self.loading_animation()
    
    def loading_animation(self):
        if not self.loading:
            return
            
        self.loading_dots = (self.loading_dots % 3) + 1
        dots = "." * self.loading_dots
        
        self.canvas.itemconfig(self.quote_text, text=f"Loading{dots}")
        self.root.after(500, self.loading_animation)
    
    def _stop_loading_animation(self):
        self.loading = False
    
    def previous_quote(self):
        if self.current_quote_index > 0:
            self.current_quote_index -= 1
            quote = self.quotes_history[self.current_quote_index]
            self._update_quote_display(quote)
            self.status_var.set(f"Showing quote {self.current_quote_index + 1} of {len(self.quotes_history)}")
            self._update_favorite_button()
    
    def next_quote(self):
        if self.current_quote_index < len(self.quotes_history) - 1:
            self.current_quote_index += 1
            quote = self.quotes_history[self.current_quote_index]
            self._update_quote_display(quote)
            self.status_var.set(f"Showing quote {self.current_quote_index + 1} of {len(self.quotes_history)}")
            self._update_favorite_button()
    
    def toggle_favorite(self):
        if not self.quotes_history:
            return
            
        current_quote = self.quotes_history[self.current_quote_index]
        
        if current_quote in self.favorite_quotes:
            self.favorite_quotes.remove(current_quote)
            self.status_var.set("Removed from favorites")
            self.fav_button.config(text="♡")
        else:
            self.favorite_quotes.append(current_quote)
            self.status_var.set("Added to favorites")
            self.fav_button.config(text="♥")
    
    def _update_favorite_button(self):
        if not self.quotes_history:
            return
            
        current_quote = self.quotes_history[self.current_quote_index]
        
        if current_quote in self.favorite_quotes:
            self.fav_button.config(text="♥")
        else:
            self.fav_button.config(text="♡")
    
    def save_quote(self):
        if not self.quotes_history:
            self.status_var.set("No quotes to save")
            return
            
        current_quote = self.quotes_history[self.current_quote_index]
        
        try:
            with open("kanye_quotes.txt", "a") as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"[{timestamp}] {current_quote}\n\n")
            
            self.status_var.set("Quote saved to kanye_quotes.txt")
        except Exception as e:
            self.status_var.set(f"Error saving quote: {str(e)}")
    
    def show_favorites(self):
        if not self.favorite_quotes:
            self.status_var.set("No favorite quotes yet")
            return
            
        fav_window = Toplevel(self.root)
        fav_window.title("Favorite Kanye Quotes")
        fav_window.config(padx=20, pady=20, bg="#121212")
        fav_window.minsize(400, 300)
        
        title_label = Label(fav_window, 
                           text="YOUR FAVORITE KANYE WISDOM", 
                           font=("Helvetica", 16, "bold"), 
                           fg="#FFD700", 
                           bg="#121212")
        title_label.pack(pady=(0, 20))
        
        quotes_frame = Frame(fav_window, bg="#1E1E1E", padx=15, pady=15)
        quotes_frame.pack(fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(quotes_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        quotes_text = Text(quotes_frame, 
                          wrap=WORD, 
                          font=("Arial", 12),
                          bg="#1E1E1E", 
                          fg="white",
                          yscrollcommand=scrollbar.set)
        quotes_text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=quotes_text.yview)
        

        for i, quote in enumerate(self.favorite_quotes):
            quotes_text.insert(END, f"{i+1}. {quote}\n\n")
        
        quotes_text.config(state=DISABLED)
        

        close_button = Button(
            fav_window, 
            text="Close", 
            command=fav_window.destroy,
            font=("Arial", 12),
            bg="#333333", 
            fg="white",
            padx=10, 
            pady=5
        )
        close_button.pack(pady=15)
    
    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_var.set(current_time)
    
    def time_updater(self):
        while True:
            self.root.after(0, self.update_time)
            time.sleep(1)

if __name__ == "__main__":
    root = Tk()
    app = KanyeQuotesApp(root)
    root.mainloop()
