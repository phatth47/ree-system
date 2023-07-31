import sys
from PySide6.QtWidgets import QApplication
from gui import FaceMatchApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Khởi tạo và hiển thị ứng dụng FaceMatchApp
    face_match_app = FaceMatchApp()
    face_match_app.show()

    sys.exit(app.exec_())
