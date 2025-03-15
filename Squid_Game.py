from tkinter import *
from PIL import Image, ImageTk,ImageDraw,ImageSequence
import pygame
import random
from tkinter import messagebox
# for including audio
pygame.mixer.init()
# creating intro window
win = Tk()
win.title("Squid-Game")
win.iconbitmap("images/images.ico")
win.state('zoomed')

canvas = Canvas(win, height=50, bg="black", highlightthickness=0)
canvas.pack(fill=X)
def show_help():
    messagebox.showinfo(title="Help", message="Welcome to the Squid Game-inspired Python game! This game features three thrilling mini-games, each testing your skills and strategy. No spoilers here—just jump in and enjoy the challenge. Good luck!")

def show_info():
    messagebox.showinfo(title="Game Info", message="This game is developed in Python using Tkinter for the GUI and Pygame for audio effects. Immerse yourself in this exciting experience and have fun!")

# Create Help Button
help_button = Button(win, text="Help", command=show_help, fg="white", bg="black",font=('Arial',15,'bold'))
help_window = canvas.create_window(150, 25, window=help_button)

# Create Info Button
info_button = Button(win, text="Info", command=show_info, fg="white", bg="black", border=0,font=('Arial',15,'bold'))
info_window = canvas.create_window(50, 25, window=info_button)


intro_music=pygame.mixer.Sound("audios/intro.mp3")
intro_music.play()
image = Image.open("images/image.gif")
photo = ImageTk.PhotoImage(image)

frame = Frame(win,bg="black")
frame.pack(pady=40,)
win.config(bg="black")
header=Canvas(win,height=4)

def Red_light_Green_light():
    global first_game_end  
    first_game_end = False

    # Show game introduction
    start_game = messagebox.askyesno(
        message="This is a Red Light-Green Light Game. Don't get caught moving during Red Light! Do You Want to Play?",
        title="Game Start"
    )
    
    if not start_game:
        return

    # Stop intro music and load game sounds
    intro_music.stop()
    song = pygame.mixer.Sound("audios/red_light_green_light.mp3")
    bullet = pygame.mixer.Sound("audios/squid-game-gunshot.mp3")
    freeze = pygame.mixer.Sound("audios/freeze.mp3")

    # Create game window
    first_game = Toplevel(win)
    first_game.iconbitmap('images/this.ico')
    first_game.title("Red Light-Green Light")
    first_game.state('zoomed')

    # Load and set background image
    image = Image.open("images/ground.jpg")
    ground_image = ImageTk.PhotoImage(image)
    ground = Canvas(first_game, width=900, height=700)
    ground.pack(fill='both', expand=True)
    ground.create_image(0, 0, image=ground_image, anchor='nw')
    first_game.ground_image = ground_image

    # Load doll images (front & back view)
    doll_front = Image.open("images/doll-front.jpg")
    doll_back = Image.open("images/doll-back.jpg")
    doll_front.thumbnail((500, 1000), Image.LANCZOS)
    doll_back.thumbnail((500, 1000), Image.LANCZOS)
    doll_front_img = ImageTk.PhotoImage(doll_front)
    doll_back_img = ImageTk.PhotoImage(doll_back)

    # Draw finish line
    ground.create_line(0, 100, 1900, 100, fill="black", width=3)

    # Main character setup
    x, y = 500, 650
    radius = 25
    main_character = ground.create_oval(x - radius, y - radius, x + radius, y + radius, fill="", outline="black", width=3)
    
    # Load and create circular player image
    char = Image.open("images/main.jpg")
    char.thumbnail((60, 60), Image.LANCZOS)
    mask = Image.new("L", char.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, char.size[0], char.size[1]), fill=255)
    circular_char = Image.new("RGBA", char.size)
    circular_char.paste(char, (0, 0), mask)
    char_image = ImageTk.PhotoImage(circular_char)
    img_move = ground.create_image(x, y, image=char_image)
    ground.char_image = char_image

    # Red/Green light label
    light_label = Label(first_game, text="", height=130, width=400, foreground="white", font=('Arial', 15),
                         image=doll_front_img, compound="center")
    ground.create_window(700, 30, window=light_label)

    # Timer setup
    global count
    count = 30
    time_label = Label(first_game, text=f"0:{count}", height=3, width=15, font=('Arial', 20), background='black', foreground='red')
    ground.create_window(100, 30, window=time_label)
    
    # Function to decrease timer
    def count_dec():
        global count
        if count > 0:
            count -= 1
            time_label.config(text=f"0:{count}")
            first_game.after(1000, count_dec)
        else:
            first_game.destroy()
            messagebox.showerror(title="Game Over", message="You Ran Out of Time")

    # Create NPC players
    npc_players = []
    total_players = 50
    players_per_row = 22
    spacing_x = 70
    spacing_y = 60
    start_x = 40
    start_y = 600
    
    for index in range(total_players):
        row = index // players_per_row
        col = index % players_per_row
        x_pos = start_x + (col * spacing_x)
        y_pos = start_y + (row * spacing_y)
        player = ground.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill="green", outline="white")
        player_text = ground.create_text(x_pos, y_pos, text=f"{index+1}", font=('Arial', 20, 'bold'), fill="white")
        npc_players.append((player, player_text))

    global is_green_light
    is_green_light = False
    
    # NPC players movement
    def player_movements():
        for players, player_text in npc_players:
            if ground.type(players) and ground.type(player_text):
                coords = ground.coords(players)
                _, y, _, _ = coords
                if y > 100:
                    if is_green_light:
                        move_distance = -random.randint(3, 10)
                        ground.move(players, 0, move_distance)
                        ground.move(player_text, 0, move_distance)
                    elif random.randint(1, 150) < 2:
                        move_distance = -random.randint(1, 5)
                        ground.move(players, 0, move_distance)
                        ground.move(player_text, 0, move_distance)
                        bullet.play()
                        ground.delete(players)
                        ground.delete(player_text)
                        npc_players.remove((players, player_text))
        first_game.after(150, player_movements)

    # Light switching function
    def light():
        global is_green_light
        is_green_light = not is_green_light
        if is_green_light:
            light_label.config(text="GREEN LIGHT", image=doll_back_img, compound='center', foreground="green")
            light_label.image = doll_back_img
            song.play()
        else:
            freeze.play()
            light_label.config(text="RED LIGHT", image=doll_front_img, foreground="red")
            light_label.image = doll_front_img
        first_game.after(5000, light)
    
    # Move character function
    def char_move():
        ground.move(main_character, 0, -15)
        ground.move(img_move, 0, -15)
        if not is_green_light:
            first_game.destroy()
            messagebox.showerror(title="Game Over", message="You Moved During Red Light!")
            return
    
    character_movement = Button(first_game, text="Move", bg="black", foreground="white", height=2, width=8, font=('Arial', 15, 'bold'), command=char_move)
    ground.create_window(1200, 50, window=character_movement)

    # Check if main player reaches the finish line
    def check_main_player_position():
        try:
         coords = ground.coords(main_character)
         if coords and coords[1] < 100:
            first_game.destroy()
            song.stop()
            global first_game_end
            first_game_end = messagebox.askyesno("You Win!", "You reached the finish line! Next game: Tic-Tac-Toe. Want to play?")
            if first_game_end:
                Tic_Tak_Toe()
        except:
            pass
        first_game.after(70, check_main_player_position)

    # Start game loops
    light()
    player_movements()
    count_dec()
    check_main_player_position()

def Rock_Paper_Scissor_minus_one():
    # Stop intro music and play new game music
    intro_music.stop()
    second_music = pygame.mixer.Sound("audios/squid_games_3.mp3")
    second_music.play()
    
    # Initialize game window
    rps = Toplevel(win)
    rps.title('Rock-Paper-Scissor-Minus-One')
    rps.resizable(False, False)
    main_shape = Canvas(rps, height=600, width=600, bg="white")
    
    # Load background image
    rps_bg = Image.open("images/dalgona_img.jpg")
    rps_bg.thumbnail((1750, 600), Image.LANCZOS)
    ground_image = ImageTk.PhotoImage(rps_bg)
    main_shape.create_image(0, 0, image=ground_image, anchor='nw')
    rps.ground_image = ground_image
    main_shape.pack()
    
    # Heading label
    heading = Label(rps, text="Take Two Choices", font=('Arial', 25, 'bold'), bg="black", fg="white")
    main_shape.create_window(300, 30, window=heading)
    
    # Frame for buttons
    buttons = Frame(rps)
    opponent_show = Label(rps, text="", bg="black", fg="white")
    main_shape.create_window(300, 300, window=opponent_show)
    
    # Load images for Rock, Paper, and Scissors
    def load_image(file, size):
        img = Image.open(file)
        img.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    
    rock_image = load_image("images/rock.png", (150, 150))
    paper_image = load_image("images/paper.png", (300, 300))
    scissors_image = load_image("images/scissors.jpg", (150, 150))
    
    # Lists to store choices
    user_choice = []
    opponent_choice = []
    var = StringVar(value="Triangle")
    
    # Function to determine the winner
    def get_selected_text():
        selected_value = var.get()
        selected_text = selected_value.split("_")[0]  # Extract choice text
        a = user_choice.index(selected_text)
        user_choice.pop(1 if a == 0 else 0)  # Remove one choice
        opponent_choice.pop(random.randint(0, 1))  # Randomly remove opponent's choice
        
        play = True
        while play:
            if (user_choice[0] == "Rock" and opponent_choice[0] == "Scissors") or \
               (user_choice[0] == "Paper" and opponent_choice[0] == "Rock") or \
               (user_choice[0] == "Scissors" and opponent_choice[0] == "Paper"):
                messagebox.showinfo(title="You Win", message=f"You win! You selected {user_choice[0]} against {opponent_choice[0]}")
                second_music.stop()
                rps.destroy()
                play = False
                prize()
            elif (user_choice[0] == "Rock" and opponent_choice[0] == "Paper") or \
                 (user_choice[0] == "Paper" and opponent_choice[0] == "Scissors") or \
                 (user_choice[0] == "Scissors" and opponent_choice[0] == "Rock"):
                messagebox.showerror(title="Game Over", message=f"You Lose! Opponent selected {opponent_choice[0]}")
                second_music.stop()
                rps.destroy()
                play = False
            elif user_choice[0] == opponent_choice[0]:
                messagebox.showinfo(message="It's a tie! Play again")
                second_music.stop()
                rps.destroy()
                Rock_Paper_Scissor_minus_one()
                play = False
    
    # Function to display selection options
    def select_winner():
        y_pos = 400
        for choice in user_choice:
            val = f"{choice}_{y_pos}"
            radio = Radiobutton(rps, text=choice, variable=var, value=val, font=('Arial', 20, 'bold'), width=7)
            main_shape.create_window(300, y_pos, window=radio)
            y_pos += 50
        submit_btn = Button(rps, text="Submit", font=('Arial', 15, 'bold'), command=get_selected_text, bg="black", fg="white")
        main_shape.create_window(300, y_pos + 50, window=submit_btn)
    
    # Disable buttons after selecting two choices
    def disable_btn():
        if len(user_choice) >= 2:
            btn1.config(state=DISABLED)
            btn2.config(state=DISABLED)
            btn3.config(state=DISABLED)
            opponent_show.config(text=f"Opponent choices: {opponent_choice[0]} and {opponent_choice[1]}", font=('Arial', 15, 'bold'))
            select_winner()
    
    # Function to handle user's choice selection
    def user_choices(btn):
        user_choice.append(btn.cget('text'))
        disable_btn()
    
    # Function to generate opponent's random choices
    def opponent_choices():
        choices = ['Rock', 'Paper', 'Scissors']
        for _ in range(2):
            opponent_choice.append(random.choice(choices))
    
    opponent_choices()
    
    # Create buttons for Rock, Paper, and Scissors
    btn1 = Button(buttons, text="Rock", height=150, width=160, font=('Arial', 15, 'bold'), image=rock_image, command=lambda: user_choices(btn1))
    btn1.grid(row=0, column=0, padx=5, pady=5)
    btn1.image = rock_image
    
    btn2 = Button(buttons, text="Paper", height=150, width=160, font=('Arial', 15, 'bold'), image=paper_image, command=lambda: user_choices(btn2))
    btn2.grid(row=0, column=1, padx=5, pady=5)
    btn2.image = paper_image
    
    btn3 = Button(buttons, text="Scissors", height=150, width=160, font=('Arial', 15, 'bold'), image=scissors_image, command=lambda: user_choices(btn3))
    btn3.grid(row=0, column=2, padx=5, pady=5)
    btn3.image = scissors_image
    
    buttons.pack(ipadx=100, ipady=10)
    main_shape.create_window(300, 200, window=buttons)
    
global tic_tac_toe_won
tic_tac_toe_won=False

def Tic_Tak_Toe():
    """
    Function to initialize and run a game of Tic-Tac-Toe.
    The player competes against the computer.
    """
    # Stop any previously playing music and start new game music
    intro_music.stop()
    third_music = pygame.mixer.Sound("audios/squid_game_intro.mp3")
    third_music.play()
    
    # Load and resize background image
    last_game_bg = Image.open("images/third.jpg")
    last_game_bg.thumbnail((500, 800), Image.LANCZOS)
    last_game_bg_img = ImageTk.PhotoImage(last_game_bg)
    
    # Load and resize player and opponent icons
    player_icon = Image.open("images/circle.webp").resize((140, 140), Image.LANCZOS)
    player_icon_img = ImageTk.PhotoImage(player_icon)
    
    opponent_icon = Image.open("images/triangle.jpg").resize((140, 140), Image.LANCZOS)
    opponent_icon_img = ImageTk.PhotoImage(opponent_icon)
    
    # Initialize game window
    last_game = Toplevel(win)
    last_game.title("Tic-Tac-Toe")
    last_game.resizable(False, False)
    last_game.iconbitmap("images/tic-tak-toe.ico")
    
    # Create main game canvas
    main_canvas = Canvas(last_game, height=600, width=500)
    main_canvas.pack()
    main_canvas.create_image(0, 0, image=last_game_bg_img, anchor='nw')
    main_canvas.last_game_bg_img = last_game_bg_img  # Prevents garbage collection issue
    
    # Game title
    heading = Label(last_game, text="Tic-Tac-Toe", font=('Arial', 30, 'bold'), background="black", foreground="light green")
    main_canvas.create_window(250, 40, window=heading)
    
    # Create a frame for the Tic-Tac-Toe grid
    frame = Frame(last_game)
    main_canvas.create_window(250, 300, window=frame)
    
    # Initialize buttons for the game grid
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            btn = Button(frame, height=8, width=20, command=lambda b=i*3+j: player_move(b))
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)
    
    # Flatten button list for easier access by index
    all_buttons = [btn for row in buttons for btn in row]
    
    # Define all possible winning patterns
    win_patterns = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # Rows
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  # Columns
        {0, 4, 8}, {2, 4, 6}             # Diagonals
    ]
    
    # Track player and opponent choices
    player_choices = set()
    opponent_choices = set()
    
    def check_winner():
        """Check if there's a winner or a tie."""
        for pattern in win_patterns:
            if pattern.issubset(player_choices):
                response = messagebox.askyesno("Game Over", "You Won! Next game: Rock-Paper-Scissor Minus One. Continue?")
                last_game.destroy()
                third_music.stop()
                if response:
                    Rock_Paper_Scissor_minus_one()
                return True
            elif pattern.issubset(opponent_choices):
                messagebox.showerror("Game Over", "You Lose!")
                last_game.destroy()
                third_music.stop()
                return True
        
        # Check for a tie
        if len(player_choices) + len(opponent_choices) == 9:
            messagebox.showinfo("Game Over", "It's a Tie! Play again.")
            last_game.destroy()
            third_music.stop()
            Tic_Tak_Toe()
            return True
        return False
    
    def opponent_move():
        """Generate and process opponent's move."""
        available_moves = [i for i in range(9) if i not in player_choices and i not in opponent_choices]
        if available_moves:
            move = random.choice(available_moves)
            btn = all_buttons[move]
            btn.config(height=120, width=140, image=opponent_icon_img, state=DISABLED)
            btn.image = opponent_icon_img
            opponent_choices.add(move)
            check_winner()
    
    def player_move(index):
        """Handle player's move when they click a button."""
        btn = all_buttons[index]
        btn.config(height=120, width=140, image=player_icon_img, state=DISABLED)
        btn.image = player_icon_img
        player_choices.add(index)
        
        if not check_winner():
            opponent_move()

def prize():
    prize_money = Toplevel(win)
    prize_money.title("Congratulations!")
    prize_money.resizable(False, False)
    prize_money.geometry("500x400")
    
    # Play sound
    prize_music = pygame.mixer.Sound("audios/7_crore_meme_sound_kbc.mp3")
    prize_music.play()   

    bg_image = Image.open("images/prize.jpg")
    bg_image.thumbnail((800, 1200), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas = Canvas(prize_money, width=500, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')
    canvas.bg_photo = bg_photo 
    label = Label(prize_money, text="You Won ₹7 Crore!", font=("Arial", 26, "bold"),
                  fg="gold", bg="black", padx=10, pady=5)
    canvas.create_window(250, 120, window=label)

    thank_you_label = Label(prize_money, text="Thank You for Playing!", font=("Arial", 16),
                            fg="white", bg="black")
    canvas.create_window(250, 170, window=thank_you_label)
    creator_label = Label(prize_money, text="Made by Krishna", font=("Arial", 14, "italic"),
                          fg="lightgray", bg="black")
    canvas.create_window(250, 320, window=creator_label)
    exit_btn = Button(prize_money, text="OK", font=("Arial", 16, "bold"), bg="red", fg="white",
                      command=prize_money.destroy)
    canvas.create_window(250, 250, window=exit_btn)
    start_button.config(state="normal")
  
start_button = Button(frame, text="Start",bg="black",foreground="white",height=1,width=8,font=30,command= Red_light_Green_light)
start_button.pack()       
      
bg = Label(frame, image=photo)
bg.pack(pady=30)
win.mainloop()
