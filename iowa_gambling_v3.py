import sys
import os
import random
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt

class IowaGamblingTaskGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.init_game()

    def initUI(self):
        self.setWindowTitle('Iowa Gambling Task')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.student_name = ""
        self.study_batch = ""
        self.gender = ""
        self.round_num = 0
        self.choices = []
        self.total_money = 2000

        self.result_label = QLabel("", self)
        self.money_label = QLabel(f'Money: ${self.total_money}', self)

        self.result_label.setAlignment(Qt.AlignCenter)
        self.money_label.setAlignment(Qt.AlignCenter)

        self.result_label.setStyleSheet("font-size: 16px; color: #333333;")
        self.money_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #005CAF;")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.result_label)
        self.vbox.addWidget(self.money_label)

        self.deck_buttons = []

        for i in range(4):
            deck_button = QPushButton(f'Deck {i + 1}', self)
            deck_button.clicked.connect(lambda checked, i=i: self.on_deck_click(i))
            deck_button.setStyleSheet("background-color: #E64A19; color: white;")
            self.deck_buttons.append(deck_button)
            self.vbox.addWidget(deck_button)

        self.setLayout(self.vbox)

        self.input_window()

    def input_window(self):
        self.input_label = QLabel('Enter Student Information:', self)
        self.name_input_label = QLabel('Enter your name:', self)
        self.name_input = QLineEdit(self)
        self.batch_input_label = QLabel('Enter your batch:', self)
        self.batch_input = QLineEdit(self)
        self.gender_input_label = QLabel('Select your gender:', self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(['Male', 'Female', 'Prefer not to say'])

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("background-color: #00A0B0; color: white;")

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.name_input_label)
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.batch_input_label)
        input_layout.addWidget(self.batch_input)
        input_layout.addWidget(self.gender_input_label)
        input_layout.addWidget(self.gender_input)
        input_layout.addWidget(self.start_button)

        self.vbox.addLayout(input_layout)

    def init_game(self):
        self.deck_rewards = [
            {'win': [100, 200], 'lose': [-350, -300]},  # Deck A: Can win 100 or 500, lose -350 or -300
            {'win': [100, 200], 'lose': [-350, -300]},  # Deck B: Can win 100 or 500, lose -350 or -300
            {'win': [50, 100], 'lose': [-25, -50]},     # Deck C: Can win 50 or 100, lose -25 or -50
            {'win': [50, 100], 'lose': [-25, -50]}       # Deck D: Can win 50 or 100, lose -25 or -50
        ]

    def start_game(self):
        self.student_name = self.name_input.text()
        self.study_batch = self.batch_input.text()
        self.gender = self.gender_input.currentText()

        self.input_label.hide()
        self.name_input_label.hide()
        self.batch_input_label.hide()
        self.gender_input_label.hide()

        self.clear_input_window()
        self.update_labels()

    def clear_input_window(self):
        self.name_input.deleteLater()
        self.batch_input.deleteLater()
        self.gender_input.deleteLater()
        sender = self.sender()
        sender.deleteLater()

    def on_deck_click(self, deck_index):
        if self.round_num < 100:
            win_amount = random.choice(self.deck_rewards[deck_index]['win'])
            lose_amount = random.choice(self.deck_rewards[deck_index]['lose'])

            win_message = f'You won: ${win_amount}'
            lose_message = f'You lost: ${-lose_amount}'

            self.total_money = self.total_money + win_amount + lose_amount
            self.choices.append(deck_index)  # Add the chosen deck index to choices

            self.round_num += 1

            self.update_labels()
            self.display_result(win_message, lose_message)
            self.save_to_csv()  # Save total money after each round

            if self.round_num == 100:
                self.save_to_csv()
                self.show_thank_you_message()

    def show_thank_you_message(self):
        for button in self.deck_buttons:
            button.hide()

        self.result_label.hide()
        self.money_label.hide()

        thank_you_label = QLabel('Thank you for participation!', self)
        thank_you_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #009688;")
        self.vbox.addWidget(thank_you_label)

    def update_labels(self):
        self.money_label.setText(f'Money: ${self.total_money}')

    def display_result(self, win_message, lose_message):
        result_text = f'{win_message}\n{lose_message}'
        self.result_label.setText(result_text)

    def save_to_csv(self):
        output_dir = "./data"  # Change to a relative path for portability
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{self.student_name}_{self.study_batch}.csv")

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Study Batch", "Gender", "Choice", "Good Choice", "Total Money"])

            for i, choice in enumerate(self.choices):
                good_choice = 1 if choice >= 2 else 0
                writer.writerow([self.student_name, self.study_batch, self.gender, choice + 1, good_choice, self.total_money])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IowaGamblingTaskGUI()
    window.show()
    sys.exit(app.exec_())
