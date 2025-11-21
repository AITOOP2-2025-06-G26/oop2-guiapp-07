import sys
import threading

from PySide6.QtWidgets import QApplication

from src.camera import CameraViewer
from GUI import MainWindow


def main() -> None:
    camera = CameraViewer()
    threading.Thread(target=camera.run, daemon=True).start()

    app = QApplication(sys.argv)
    win = MainWindow(camera)
    win.show()
    exit_code = app.exec()

    camera.stop()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()