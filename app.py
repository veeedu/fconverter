import sys, os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QListWidget,
    QComboBox, QListWidgetItem, QHBoxLayout, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from pathlib import Path
from converters import audio, video, image, document
from utils import get_output_dir

FORMAT_MAP = {
    ".png": ["jpg", "webp", "bmp", "gif", "tiff"],
    ".jpg": ["png", "webp", "bmp", "gif", "tiff"],
    ".jpeg": ["png", "webp", "bmp", "gif", "tiff"],
    ".bmp": ["jpg", "png", "webp", "gif", "tiff"],
    ".gif": ["jpg", "png", "webp", "bmp", "tiff"],
    ".tiff": ["jpg", "png", "webp", "bmp", "gif"],
    ".webp": ["jpg", "png", "bmp", "gif", "tiff"],
    ".mp3": ["wav", "ogg", "aac", "flac"],
    ".wav": ["mp3", "ogg", "aac", "flac"],
    ".aac": ["mp3", "wav", "ogg", "flac"],
    ".flac": ["mp3", "wav", "ogg", "aac"],
    ".ogg": ["mp3", "wav", "aac", "flac"],
    ".mp4": ["mkv", "avi", "mov", "flv", "wmv"],
    ".mkv": ["mp4", "avi", "mov", "flv", "wmv"],
    ".avi": ["mp4", "mkv", "mov", "flv", "wmv"],
    ".mov": ["mp4", "mkv", "avi", "flv", "wmv"],
    ".flv": ["mp4", "mkv", "avi", "mov", "wmv"],
    ".wmv": ["mp4", "mkv", "avi", "mov", "flv"],
    ".pdf": ["txt"],
    ".docx": ["txt"]
}

CONVERTER_MAP = {
    ".mp3": audio,
    ".wav": audio,
    ".aac": audio,
    ".flac": audio,
    ".ogg": audio,
    ".mp4": video,
    ".mkv": video,
    ".avi": video,
    ".mov": video,
    ".flv": video,
    ".wmv": video,
    ".png": image,
    ".jpg": image,
    ".jpeg": image,
    ".bmp": image,
    ".gif": image,
    ".tiff": image,
    ".webp": image,
    ".pdf": document,
    ".docx": document
}

class ConversionWorker(QThread):
    progress_updated = Signal(int)
    conversion_finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, files, out_fmt, output_dir):
        super().__init__()
        self.files = files
        self.out_fmt = out_fmt
        self.output_dir = output_dir

    def run(self):
        total = len(self.files)
        for i, path in enumerate(self.files):
            try:
                ext = Path(path).suffix.lower()
                converter = CONVERTER_MAP.get(ext)
                if converter:
                    output_path = self.output_dir / (Path(path).stem + "." + self.out_fmt)
                    converter.convert(path, str(output_path))
                else:
                    self.error_occurred.emit(f"Unsupported format for {path}")
            except Exception as e:
                self.error_occurred.emit(f"Error converting {path}: {str(e)}")
            self.progress_updated.emit(int((i + 1) / total * 100))
        self.conversion_finished.emit()

class DropArea(QLabel):
    def __init__(self, callback):
        super().__init__("Drop files here or click Browse")
        self.callback = callback
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #777;
                border-radius: 16px;
                padding: 40px;
                font-size: 16px;
            }
        """)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        self.callback(files)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Converter")
        self.resize(800, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.drop = DropArea(self.add_files)
        layout.addWidget(self.drop)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.status = QLabel("")
        layout.addWidget(self.status)

        bottom = QHBoxLayout()

        self.format_box = QComboBox()
        self.format_box.addItem("Select output format")
        bottom.addWidget(self.format_box)

        browse = QPushButton("Browse files")
        browse.clicked.connect(self.open_files)
        bottom.addWidget(browse)

        convert = QPushButton("Convert")
        convert.clicked.connect(self.convert_files)
        self.convert_btn = convert
        bottom.addWidget(convert)

        layout.addLayout(bottom)

    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files")
        self.add_files(files)

    def add_files(self, files):
        for f in files:
            if not f:
                continue
            item = QListWidgetItem(f)
            self.file_list.addItem(item)

        self.update_formats()

    def update_formats(self):
        self.format_box.clear()
        exts = set(os.path.splitext(self.file_list.item(i).text())[1].lower()
                   for i in range(self.file_list.count()))
        formats = set()
        for e in exts:
            formats.update(FORMAT_MAP.get(e, []))

        self.format_box.addItems(sorted(formats) or ["No formats available"])

    def convert_files(self):
        out_fmt = self.format_box.currentText()
        if not out_fmt or out_fmt.startswith("No") or out_fmt == "Select output format":
            self.status.setText("Please select a valid output format.")
            return

        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            self.status.setText("No files to convert.")
            return

        output_dir = get_output_dir()
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status.setText("Converting...")
        self.convert_btn.setEnabled(False)

        self.worker = ConversionWorker(files, out_fmt, output_dir)
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.conversion_finished.connect(self.on_conversion_finished)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

    def on_conversion_finished(self):
        self.progress.setVisible(False)
        self.status.setText("Conversion completed. Files saved to " + str(get_output_dir()))
        self.convert_btn.setEnabled(True)

    def on_error(self, msg):
        self.status.setText(msg)
        self.convert_btn.setEnabled(True)

app = QApplication(sys.argv)
w = ConverterApp()
w.show()
sys.exit(app.exec())
