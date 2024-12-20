import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import random

# Character class with priority, health, and attack power
class Character:
    def __init__(self, name, priority, attack_power, canvas, x, y, color):
        self.name = name
        self.priority = priority
        self.health = 100
        self.attack_power = attack_power
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.visual = canvas.create_rectangle(x, y, x + 50, y + 50, fill=color)
        self.grave = None

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = random.randint(1, self.attack_power)
        target.health -= damage
        return f"{self.name} attacks {target.name} for {damage} damage. {target.name} has {max(0, target.health)} health left."

    def move_toward(self, target):
        self.canvas.move(self.visual, (target.x - self.x) / 4, 0)
        self.canvas.update()

    def move_back(self):
        self.canvas.move(self.visual, (self.x - self.canvas.coords(self.visual)[0]), 0)
        self.canvas.update()

    def flash(self):
        self.canvas.itemconfig(self.visual, fill='yellow')
        self.canvas.update()
        time.sleep(0.1)
        self.canvas.itemconfig(self.visual, fill=self.color)
        self.canvas.update()

    def show_grave(self):
        self.canvas.delete(self.visual)
        self.grave = self.canvas.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, fill='gray')
        self.canvas.create_text(self.x + 25, self.y + 25, text="RIP", fill='white')

# GUI class
class FightGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sword Fight Game - Dark Theme")
        self.root.configure(bg="#1e1e1e")

        # Main canvas for visualizing the fight
        self.canvas = tk.Canvas(root, width=600, height=400, bg='#2e2e2e', highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Create characters with default priorities and attack powers
        self.character1 = Character("Knight", priority=3, attack_power=10, canvas=self.canvas, x=100, y=150, color='#3a86ff')
        self.character2 = Character("Samurai", priority=2, attack_power=12, canvas=self.canvas, x=450, y=150, color='#ff006e')

        # Frame for priority inputs
        input_frame = tk.Frame(root, bg='#1e1e1e')
        input_frame.grid(row=1, column=0, columnspan=4, pady=10)

        tk.Label(input_frame, text="Knight Priority:", fg='white', bg='#1e1e1e').grid(row=0, column=0, padx=5)
        self.priority1_entry = tk.Entry(input_frame, bg='#3b3b3b', fg='white', insertbackground='white', highlightbackground='#3b3b3b')
        self.priority1_entry.insert(0, str(self.character1.priority))
        self.priority1_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Samurai Priority:", fg='white', bg='#1e1e1e').grid(row=0, column=2, padx=5)
        self.priority2_entry = tk.Entry(input_frame, bg='#3b3b3b', fg='white', insertbackground='white', highlightbackground='#3b3b3b')
        self.priority2_entry.insert(0, str(self.character2.priority))
        self.priority2_entry.grid(row=0, column=3, padx=5)

        # Frame for buttons
        button_frame = tk.Frame(root, bg='#1e1e1e')
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.start_button = tk.Button(button_frame, text="Start Fight", command=self.start_fight, bg='#444444', fg='white', activebackground='#555555', activeforeground='white')
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop Fight", command=self.stop_fight, bg='#444444', fg='white', activebackground='#555555', activeforeground='white')
        self.stop_button.grid(row=0, column=1, padx=5)

        self.restart_button = tk.Button(button_frame, text="Restart Fight", command=self.restart_fight, bg='#444444', fg='white', activebackground='#555555', activeforeground='white')
        self.restart_button.grid(row=0, column=2, padx=5)

        # Log area for displaying fight progress
        self.log = scrolledtext.ScrolledText(root, width=60, height=10, bg='#3b3b3b', fg='white', state='disabled', insertbackground='white')
        self.log.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        self.fight_thread = None
        self.fight_running = False

    def log_action(self, action):
        self.log.config(state='normal')
        self.log.insert(tk.END, action + "\n")
        self.log.yview(tk.END)
        self.log.config(state='disabled')

    def update_health_bars(self):
        health_ratio1 = self.character1.health / 100
        health_ratio2 = self.character2.health / 100
        self.canvas.coords(self.character1.visual, self.character1.x, self.character1.y,
                           self.character1.x + 50 * health_ratio1, self.character1.y + 50)
        self.canvas.coords(self.character2.visual, self.character2.x, self.character2.y,
                           self.character2.x + 50 * health_ratio2, self.character2.y + 50)

    def fight(self):
        self.fight_running = True
        while self.character1.is_alive() and self.character2.is_alive() and self.fight_running:
            total_priority = self.character1.priority + self.character2.priority
            attack_chance = random.uniform(0, total_priority)

            if attack_chance <= self.character1.priority:
                self.character1.move_toward(self.character2)
                time.sleep(0.2)
                action = self.character1.attack(self.character2)
                self.log_action(action)
                self.character1.move_back()
                self.character2.flash()
                self.update_health_bars()
                if not self.character2.is_alive():
                    self.log_action(f"{self.character2.name} has been defeated!")
                    self.character2.show_grave()
                    self.display_winner(self.character1.name)
                    break

            else:
                self.character2.move_toward(self.character1)
                time.sleep(0.2)
                action = self.character2.attack(self.character1)
                self.log_action(action)
                self.character2.move_back()
                self.character1.flash()
                self.update_health_bars()
                if not self.character1.is_alive():
                    self.log_action(f"{self.character1.name} has been defeated!")
                    self.character1.show_grave()
                    self.display_winner(self.character2.name)
                    break

            time.sleep(0.1)

        self.start_button.config(state='normal')

    def start_fight(self):
        try:
            priority1 = float(self.priority1_entry.get())
            priority2 = float(self.priority2_entry.get())
        except ValueError:
            self.log_action("Invalid priority values. Please enter numbers.")
            return

        self.character1.priority = max(0.1, priority1)
        self.character2.priority = max(0.1, priority2)

        self.start_button.config(state='disabled')
        self.fight_thread = threading.Thread(target=self.fight)
        self.fight_thread.start()

    def stop_fight(self):
        self.fight_running = False
        if self.fight_thread is not None:
            self.log_action("The fight has been stopped.")
            self.start_button.config(state='normal')

    def restart_fight(self):
        self.stop_fight()
        self.canvas.delete("all")
        self.character1 = Character("Knight", priority=3, attack_power=10, canvas=self.canvas, x=100, y=150, color='#3a86ff')
        self.character2 = Character("Samurai", priority=2, attack_power=12, canvas=self.canvas, x=450, y=150, color='#ff006e')
        self.log.config(state='normal')
        self.log.delete('1.0', tk.END)
        self.log.config(state='disabled')
        self.log_action("Fight restarted! Set priorities and start the fight again.")

    def display_winner(self, winner_name):
        self.canvas.create_text(300, 200, text=f"{winner_name} Wins!", font=("Arial", 24), fill="#76c893")

# Create the main window and run the game
root = tk.Tk()
game = FightGameGUI(root)
root.mainloop()
