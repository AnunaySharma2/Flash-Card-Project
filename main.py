from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
english_word = None
random_dict = None


def remove_word():
    to_learn.remove(random_dict)
    data = pandas.DataFrame(to_learn)
    data.to_csv("word_to_learn.csv", index=False)
    next_card()


def next_card():
    global english_word, flip_timer, random_dict, to_learn
    window.after_cancel(flip_timer)
    random_dict = choice(to_learn)
    french_word = random_dict["French"]
    english_word = random_dict["English"]
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=f"{french_word}", fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=f"{english_word}", fill="white")
    canvas.itemconfig(canvas_image, image=card_back)


try:
    words_to_learn_file = pandas.read_csv("word_to_learn.csv")
except FileNotFoundError:
    data_file = pandas.read_csv("data/french_words.csv")
    to_learn = pandas.DataFrame.to_dict(data_file, orient="records")
else:
    to_learn = pandas.DataFrame.to_dict(words_to_learn_file, orient="records")

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=remove_word)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
