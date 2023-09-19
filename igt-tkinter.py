import tkinter as tk
from tkinter import ttk
import random
import csv
import os

class IowaGamblingTaskGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.init_game()

    def initUI(self):
        self.title('Iowa Gambling Task')
        self.geometry('400x300')

        self.student_name = ""
        self.study_batch = ""
        self.gender = ""
        self.round_num = 0
        self.choices = []
        self.total_money = 2000

        self.result_label = tk.Label(self, text="", justify='center')
        self.money_label = tk.Label(self, text=f'Money: ${self.total_money}', justify='center')

        self.result_label.pack(pady=10)
        self.money_label.pack(pady=10)

        self.deck_buttons = []

        for i in range(4):
            deck_button = tk.Button(self, text=f'Deck {i + 1}', command=lambda i=i: self.on_deck_click(i))
            deck_button.pack(pady=5)
            self.deck_buttons.append(deck_button)

        self.input_window()

    def input_window(self):
        self.input_label = tk.Label(self, text='Enter Student Information:')
        self.input_label.pack(pady=10)

        self.name_input_label = tk.Label(self, text='Enter your name:')
        self.name_input_label.pack(pady=5)
        self.name_input = tk.Entry(self)
        self.name_input.pack(pady=5)

        self.batch_input_label = tk.Label(self, text='Enter your batch:')
        self.batch_input_label.pack(pady=5)
        self.batch_input = tk.Entry(self)
        self.batch_input.pack(pady=5)

        self.gender_input_label = tk.Label(self, text='Select your gender:')
        self.gender_input_label.pack(pady=5)
        self.gender_input = ttk.Combobox(self, values=['Male', 'Female', 'Prefer not to say'])
        self.gender_input.pack(pady=5)

        self.start_button = tk.Button(self, text='Start', command=self.start_game)
        self.start_button.pack(pady=10)

    def init_game(self):
        self.deck_rewards = [
            [100, 200, -350, -300],  # Deck A
            [100, 200, -350, -300],  # Deck B
            [50, 100, -25, 50],      # Deck C
            [100, 50, -25, 50]       # Deck D
        ]

    def start_game(self):
        self.student_name = self.name_input.get()
        self.study_batch = self.batch_input.get()
        self.gender = self.gender_input.get()

        self.input_label.pack_forget()
        self.name_input_label.pack_forget()
        self.batch_input_label.pack_forget()
        self.gender_input_label.pack_forget()

        self.clear_input_window()
        self.update_labels()
        self.clear_input_window()
        self.update_labels()

    def clear_input_window(self):
        self.name_input.destroy()
        self.batch_input.destroy()
        self.gender_input.destroy()
        self.start_button.destroy()

    def on_deck_click(self, deck_index):
        if self.round_num < 100:
            self.choices.append(deck_index)
            reward = random.choice(self.deck_rewards[deck_index])  # Randomly select a reward/punishment
            self.total_money += reward

            self.round_num += 1
            self.update_labels()
            self.display_result(reward)
            self.save_to_csv()  # Save total money after each round

            if self.round_num == 100:
                self.save_to_csv()
                self.show_thank_you_message()  # Save total money after the 100th round

    def show_thank_you_message(self):
        for button in self.deck_buttons:
            button.pack_forget()

        self.result_label.pack_forget()
        self.money_label.pack_forget()

        # Show the thank you message
        thank_you_label = tk.Label(self, text='Thank you for participation!')
        thank_you_label.pack(pady=50)

    def update_labels(self):
        self.money_label.config(text=f'Money: ${self.total_money}')
        if self.round_num < len(self.choices):
            reward = self.deck_rewards[self.choices[self.round_num]][self.round_num]

    def display_result(self, reward):
        if reward > 0:
            self.result_label.config(text=f'You won: ${reward}')
        else:
            self.result_label.config(text=f'You lost: ${-reward}')

    def save_to_csv(self):
        output_dir = "/Users/baoquynh/Downloads/Iowa gambling main/data"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{self.student_name}_{self.study_batch}.csv")

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Study Batch", "Gender", "Choice", "Good Choice", "Total Money"])

            for i, choice in enumerate(self.choices):
                good_choice = 1 if choice >= 2 else 0
                writer.writerow([self.student_name, self.study_batch, self.gender, choice + 1, good_choice, self.total_money])

if __name__ == '__main__':
    app = IowaGamblingTaskGUI()
    app.mainloop()
