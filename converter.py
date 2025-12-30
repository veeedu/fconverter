import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QListWidget, QComboBox
)
from PySide6.QtCore import Qt


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Converter")
        self.resize(700, 450)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        self.drop_label = QLabel("Drop files here or click Browse")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #777;
                border-radius: 15px;
                padding: 40px;
                font-size: 16px;
            }
        """)
        self.drop_label.setAcceptDrops(True)

        self.file_list = QListWidget()

        self.format_box = QComboBox()
        self.format_box.addItems(["Select output format"])

        browse_btn = QPushButton("Browse files")
        browse_btn.clicked.connect(self.open_files)

        convert_btn = QPushButton("Convert")

        layout.addWidget(self.drop_label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.format_box)
        layout.addWidget(browse_btn)
        layout.addWidget(convert_btn)

    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select files",
            "",
            "All files (*)"
        )
        for f in files:
            self.file_list.addItem(f)


app = QApplication(sys.argv)
window = ConverterApp()
window.show()
sys.exit(app.exec())
