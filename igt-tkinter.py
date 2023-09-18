import tkinter as tk
from tkinter import messagebox
import random
import csv
import os

class IowaGamblingTaskGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Iowa Gambling Task')
        self.window.geometry('400x300')

        self.student_name = ""
        self.study_batch = ""
        self.round_num = 0
        self.choices = []
        self.total_money = 2000
        self.deck_rewards = []

        self.result_label = tk.Label(self.window, text="")
        self.money_label = tk.Label(self.window, text=f'Money: ${self.total_money}')

        self.result_label.pack()
        self.money_label.pack()

        self.deck_buttons = []

        for i in range(4):
            deck_button = tk.Button(self.window, text=f'Deck {i + 1}', command=lambda i=i: self.on_deck_click(i))
            deck_button.pack()
            self.deck_buttons.append(deck_button)

        self.init_game()
        self.input_window()

    def input_window(self):
        input_label = tk.Label(self.window, text='Enter Student Information:')
        input_label.pack()

        self.name_input = tk.Entry(self.window)
        self.name_input.pack()

        self.batch_input = tk.Entry(self.window)
        self.batch_input.pack()

        start_button = tk.Button(self.window, text='Start', command=self.start_game)
        start_button.pack()

    def init_game(self):
        self.deck_rewards = [
            [100, 200, -350, -300],  # Deck A
            [100, 200, -350, -300],  # Deck B
            [50, 100, -25, 50],     # Deck C
            [100, 50, -25, 50]      # Deck D
        ]

    def start_game(self):
        self.student_name = self.name_input.get()
        self.study_batch = self.batch_input.get()
        self.clear_input_window()
        self.update_labels()

    def clear_input_window(self):
        self.name_input.destroy()
        self.batch_input.destroy()
        sender = self.window.nametowidget(self.window.winfo_containing(self.window.winfo_pointerx(), self.window.winfo_pointery()))
        sender.destroy()

    def on_deck_click(self, deck_index):
        if self.round_num < 100:
            self.choices.append(deck_index)
            reward = random.choice(self.deck_rewards[deck_index])  # Randomly select a reward/punishment
            self.total_money += reward

        self.round_num += 1
        if self.round_num < 100:
            self.update_labels()
            self.display_result(reward)
        else:
            self.save_to_csv()

    def update_labels(self):
        self.money_label.config(text=f'Money: ${self.total_money}')
        if self.round_num < len(self.choices):
            reward = self.deck_rewards[self.choices[self.round_num]][self.round_num]

    def display_result(self, reward):
        if reward > 0:
            self.result_label.config(text=f'You won: ${reward}')
        else:
            self.result_label.config(text=f'You lost: ${-reward}')

    def show_message(self, message):
        if hasattr(self, 'result_message'):
            self.result_message.destroy()  # Remove the previous message if it exists

        self.result_message = tk.Label(self.window, text=message)
        self.result_message.pack()

    def save_to_csv(self):
        output_dir = "/Users/baoquynh/Downloads/Iowa gambling main/data"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{self.student_name}_{self.study_batch}.csv")

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Study Batch", "Choice", "Good Choice", "Total Money"])

            for i, choice in enumerate(self.choices):
                good_choice = 1 if choice >= 2 else 0
                writer.writerow([self.student_name, self.study_batch, choice + 1, good_choice, self.total_money])

        self.window.destroy()

if __name__ == '__main__':
    app = IowaGamblingTaskGUI()
    app.window.mainloop()
