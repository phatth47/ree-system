import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget


class FaceMatchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = None
        self.face_match = False
        self.capture_image = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Face Match App")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Tạo nút "Check" để kiểm tra khuôn mặt
        check_button = QPushButton("Check")
        check_button.clicked.connect(self.on_check_button_click)
        layout.addWidget(check_button)

        # Tạo label để hiển thị kết quả
        self.result_label = QLabel("")
        # self.result_label.setFont("Arial", 18)
        layout.addWidget(self.result_label)

    def on_check_button_click(self):
        # Gọi hàm kiểm tra khuôn mặt từ file logic.py
        from logic import check_face

        # Thực hiện kiểm tra khuôn mặt và hiển thị kết quả lên label
        self.face_match, self.capture_image = check_face()

        if self.face_match:
            self.result_label.setText("True")
        else:
            self.result_label.setText("False")
