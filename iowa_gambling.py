import sys
import os
import random
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QLineEdit

class IowaGamblingTaskGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.init_game()

    def initUI(self):
        self.setWindowTitle('Iowa Gambling Task')
        self.setGeometry(100, 100, 400, 300)

        self.student_name = ""
        self.study_batch = ""
        self.round_num = 0
        self.choices = []
        self.total_money = 2000

        self.result_label = QLabel("You have", self)
        self.money_label = QLabel(f'Money: ${self.total_money}', self)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.result_label)
        self.vbox.addWidget(self.money_label)

        self.deck_buttons = []

        for i in range(4):
            deck_button = QPushButton(f'Deck {i + 1}', self)
            deck_button.clicked.connect(lambda checked, i=i: self.on_deck_click(i))
            self.deck_buttons.append(deck_button)
            self.vbox.addWidget(deck_button)

        self.setLayout(self.vbox)

        self.input_window()

    def input_window(self):
        input_label = QLabel('Enter Student Information:', self)
        self.name_input = QLineEdit(self)
        self.batch_input = QLineEdit(self)
        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start_game)

        input_layout = QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.batch_input)
        input_layout.addWidget(start_button)

        self.vbox.addLayout(input_layout)

    def init_game(self):
        self.deck_rewards = [
            [100, 200, -350, -300],  # Deck A
            [100, 200, -350, -300],  # Deck B
            [50, 100, -25, 50],     # Deck C
            [100, 50, -25, 50]      # Deck D
        ]

    def start_game(self):
        self.student_name = self.name_input.text()
        self.study_batch = self.batch_input.text()
        self.clear_input_window()
        self.update_labels()

    def clear_input_window(self):
        self.name_input.deleteLater()
        self.batch_input.deleteLater()
        sender = self.sender()
        sender.deleteLater()

    def on_deck_click(self, deck_index):
        if self.round_num < 100:
            self.choices.append(deck_index)
            reward = random.choice(self.deck_rewards[deck_index])  # Randomly select a reward/punishment
            self.total_money += reward

        self.round_num += 1
        if self.round_num < 100:
            self.update_labels()
        else:
            self.save_to_csv()

    def update_labels(self):
        self.money_label.setText(f'Money: ${self.total_money}')
        if self.round_num < len(self.choices):
            reward = self.deck_rewards[self.choices[self.round_num]][self.round_num]
            if reward > 0:
                self.show_result(f'You won ${reward}')
            else:
                self.show_result(f'You lost ${abs(reward)}')
        else:
            self.show_result('')

    def show_result(self, message):
        if hasattr(self, 'result_message'):
            self.result_message.deleteLater()  # Remove the previous message if it exists

        self.result_message = QLabel(message, self)
        self.vbox.addWidget(self.result_message)



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

        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IowaGamblingTaskGUI()
    window.show()
    sys.exit(app.exec_())
