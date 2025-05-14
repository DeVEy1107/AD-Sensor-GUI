import sys
from PyQt6.QtWidgets import QApplication
from presenter.main_presenter import Presenter
from view.main_window import MainWindow


if __name__ == "__main__":
   
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    
    # Initialize presenter with model and view
    presenter = Presenter(None, main_window)

    sys.exit(app.exec())