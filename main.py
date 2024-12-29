import sys

from PySide6.QtWidgets import QApplication

from interface import Window
from logic import Logic


def main() -> None:
    app = QApplication([])
    bll = Logic()
    window = Window(bll)
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()