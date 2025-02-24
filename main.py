from tkinter import *
import requests

def kanye_says():
    data = requests.get("https://api.kanye.rest")
    data.raise_for_status()
    quote = data.json()["quote"]
    canvas.itemconfig(text, text=quote)

window = Tk()
window.title("Kanye Says...")
window.config(padx=30, pady=30)

canvas = Canvas(height=400,width=400)
image_of_bg = PhotoImage(file="background.png")
image_canvas = canvas.create_image(200, 200, image=image_of_bg)
canvas.grid(row=0, column=0)

text = canvas.create_text(200,180,
                          text="Welcome to Kanye Says.\n The Best quotes of Kanye West",
                          font=("Arial", 19, "bold"),
                          fill="white",
                          width=250)

image_of_kanye = PhotoImage(file="kanye.png")
button = Button(image=image_of_kanye, command=kanye_says, highlightthickness=0, borderwidth=0)
button.grid(row=1,column=0)

window.mainloop()