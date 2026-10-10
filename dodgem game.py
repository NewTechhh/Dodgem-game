
import tkinter as tk
import random

# Create the game window
root = tk.Tk()
root.title("Mini Dodge Game")
root.geometry("500x550")
root.resizable(False, False)
root.configure(bg="#101827")

score = 0
running = True
blocks = []

# Title and score
title = tk.Label(
    root, text="NEON DODGE",
    font=("Arial", 22, "bold"),
    fg="#60a5fa", bg="#101827"
)
title.pack(pady=10)

score_label = tk.Label(
    root, text="Score: 0",
    font=("Arial", 14),
    fg="white", bg="#101827"
)
score_label.pack()

# Game area
canvas = tk.Canvas(
    root, width=460, height=400,
    bg="#172238", highlightthickness=0
)
canvas.pack(pady=10)

# Player
player = canvas.create_rectangle(
    210, 350, 250, 390,
    fill="#38bdf8", outline=""
)

def move_player(event):
    if not running:
        return

    if event.keysym == "Left":
        canvas.move(player, -25, 0)
    elif event.keysym == "Right":
        canvas.move(player, 25, 0)

    x1, y1, x2, y2 = canvas.coords(player)

    if x1 < 0:
        canvas.move(player, -x1, 0)
    if x2 > 460:
        canvas.move(player, 460 - x2, 0)

root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

def game_loop():
    global score, running

    if not running:
        return

    # Occasionally create a falling block
    if random.randint(1, 20) == 1:
        x = random.randint(0, 430)
        block = canvas.create_rectangle(
            x, 0, x + 30, 30,
            fill="#fb7185", outline=""
        )
        blocks.append(block)

    # Move blocks and check collisions
    player_box = canvas.coords(player)

    for block in blocks[:]:
        canvas.move(block, 0, 5)
        box = canvas.coords(block)

        if (
            player_box[0] < box[2]
            and player_box[2] > box[0]
            and player_box[1] < box[3]
            and player_box[3] > box[1]
        ):
            running = False
            canvas.create_text(
                230, 190,
                text="GAME OVER",
                fill="white",
                font=("Arial", 26, "bold")
            )
            canvas.create_text(
                230, 230,
                text=f"Final score: {score}",
                fill="#60a5fa",
                font=("Arial", 16)
            )
            return

        if box[1] > 400:
            canvas.delete(block)
            blocks.remove(block)
            score += 1
            score_label.config(text=f"Score: {score}")

    root.after(40, game_loop)

# Start the game
root.after(500, game_loop)
root.mainloop()
