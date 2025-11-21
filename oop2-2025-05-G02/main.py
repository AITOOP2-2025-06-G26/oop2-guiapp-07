import sys
import threading
from PySide6.QtWidgets import QApplication
from src.camera import CameraViewer
from src.events import setup_capture_event
from GUI import MainWindow

if __name__ == "__main__":
    camera = CameraViewer()
    threading.Thread(target=camera.run, daemon=True).start()

    app = QApplication(sys.argv)
    win = MainWindow(camera)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    camera = CameraViewer()
    threading.Thread(target=camera.run, daemon=True).start()

    app = QApplication(sys.argv)
    win = MainWindow(camera)
    win.show()
    sys.exit(app.exec())