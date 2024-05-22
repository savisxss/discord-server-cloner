from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class ServerCloneGUI(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Server Clone")

        layout = QVBoxLayout()

        self.token_label = QLabel("Discord Token:")
        layout.addWidget(self.token_label)

        self.token_entry = QLineEdit()
        layout.addWidget(self.token_entry)

        self.source_label = QLabel("Server to Copy ID:")
        layout.addWidget(self.source_label)

        self.source_entry = QLineEdit()
        layout.addWidget(self.source_entry)

        self.destination_label = QLabel("Your Server ID:")
        layout.addWidget(self.destination_label)

        self.destination_entry = QLineEdit()
        layout.addWidget(self.destination_entry)

        self.start_button = QPushButton("Start Cloning")
        self.start_button.clicked.connect(self.start_cloning)
        layout.addWidget(self.start_button)

        self.loading_label = QLabel("Cloning in progress...")
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        self.setLayout(layout)

    def start_cloning(self):
        token = self.token_entry.text().strip()
        source_id = self.source_entry.text().strip()
        destination_id = self.destination_entry.text().strip()

        if not token or not source_id or not destination_id:
            QMessageBox.critical(self, "Error", "Please fill in all the fields.")
            return

        self.start_button.setEnabled(False)
        self.loading_label.show()

        self.client.token = token
        self.client.input_guild_id = source_id
        self.client.output_guild_id = destination_id
        self.client.run(token)

        self.start_button.setEnabled(True)
        self.loading_label.hide()