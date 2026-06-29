from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget, QHBoxLayout, QFileDialog, QListWidget, QStyleFactory, QSlider, QComboBox, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
import sys

# import the individual page classes
from business_page import BusinessPage
from performance_page import PerformancePage
from forecasting_page import ForecastingPage    

# import controller
from controller import Controller

controller = Controller()

# create the main application
app = QApplication([])
app.setStyle(QStyleFactory.create("Fusion"))
app.setStyleSheet("""
    QWidget {
        background-color: #E3C397;
    }

    /* Button Styling */
    QPushButton {
        background-color: #A0522D;
        color: white;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 16px;
    }

    QPushButton:hover {
        background-color: #8B4513;
    }

    QPushButton:pressed {
        background-color: #5C3317; 
        padding-top: 12px;     
        padding-bottom: 8px;
    }

    /* Slider Styling */        
    QSlider::groove:horizontal {
    height: 6px;
    background: #D2B48C;
    border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #A0522D;
        border: none;
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }

    QSlider::handle:horizontal:hover {
        background: #8B4513;
    }

    /* Dropdown box styling */              
    QComboBox {
    background-color: white;
    border: 1px solid #C0A080;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 13px;
    }

    QComboBox::drop-down {
        border: none;
    }
                  
    /* Checkbox styling */
    QCheckBox {
        spacing: 6px;
        font-size: 13px;
    }

    QCheckBox::indicator {
        width: 14px;
        height: 14px;
        border-radius: 4px;
        border: 1px solid #A0522D;
        background: white;
    }

    QCheckBox::indicator:checked {
        background-color: #A0522D;
    }

    /* File list styling */            
    QListWidget {
    background-color: white;
    border: 1px solid #C0A080;
    border-radius: 12px;
    padding: 5px;
    font-size: 13px;
    outline: none;   
    }

    QListWidget::item {
        padding: 8px;
        border-radius: 8px;
                  
    }

    QListWidget::item:selected {
        background-color: #E3C397;
        color: black;
    }

    QListWidget::item:hover {
        background-color: #F2D5B0;
    }
                  
    /* Grey button styling */  
    QPushButton#greyButton {
    background-color: #555555;
    color: white;
    }

    QPushButton#greyButton:hover {
        background-color: #444444;
    }

    QPushButton#greyButton:pressed {
        background-color: #333333;
    }   
    """)

# create the main window
window = QWidget()
window.setWindowTitle('RoastWorks Analytics Dashboard')
window.setFixedSize(1024, 768)

# center window
screen = app.primaryScreen().availableGeometry()
x = (screen.width() - window.width()) // 2
y = (screen.height() - window.height()) // 2
window.move(x, y)

window.controller = controller
window.selected_files = []

stack = QStackedWidget()

# home page
main_page = QWidget()
layout = QVBoxLayout(main_page)

top_layout = QHBoxLayout()
image_label = QLabel()
pixmap = QPixmap('backend/icons/Logo2.png')
pixmap = pixmap.scaled(200, 200)
image_label.setPixmap(pixmap)
top_layout.addWidget(image_label)
top_layout.addStretch()

main_layout = QVBoxLayout()

file_list = QListWidget()

label = QLabel("<h1>Welcome to RoastWorks Analytics Dashboard!</h1>")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

buttonPerformance = QPushButton("Go to Sales Performance Dashboard")
buttonBusiness = QPushButton("Go to Business Performance Dashboard")
buttonForecasting = QPushButton("Go to Forecasting Dashboard")
buttonImport = QPushButton("Import CSV Files")
buttonRemove = QPushButton("Remove Selected File")

# disable pages initially
buttonPerformance.setEnabled(False)
buttonBusiness.setEnabled(False)
buttonForecasting.setEnabled(False)
buttonPerformance.setStyleSheet("background-color: grey; color: white;")
buttonBusiness.setStyleSheet("background-color: grey; color: white;")
buttonForecasting.setStyleSheet("background-color: grey; color: white;")
label.setStyleSheet("color: black;")

main_layout.addStretch()
main_layout.addWidget(label)
main_layout.addSpacing(100)
main_layout.addWidget(buttonPerformance, alignment=Qt.AlignmentFlag.AlignCenter)
main_layout.addWidget(buttonBusiness, alignment=Qt.AlignmentFlag.AlignCenter)
main_layout.addWidget(buttonForecasting, alignment=Qt.AlignmentFlag.AlignCenter)
main_layout.addStretch()
main_layout.addWidget(buttonImport, alignment=Qt.AlignmentFlag.AlignCenter)
main_layout.addWidget(file_list, alignment=Qt.AlignmentFlag.AlignCenter)
main_layout.addWidget(buttonRemove, alignment=Qt.AlignmentFlag.AlignCenter)

layout.addLayout(top_layout)
layout.addLayout(main_layout)

# pages
performance_page = PerformancePage(stack)
business_page = BusinessPage(stack)
forecasting_page = ForecastingPage(stack)

stack.addWidget(main_page)
stack.addWidget(performance_page)
stack.addWidget(business_page)
stack.addWidget(forecasting_page)

# import files
def import_file():
    file_paths, _ = QFileDialog.getOpenFileNames(
        window, "Select CSV Files", "", "CSV Files (*.csv)"
    )

    # check how many files have already been added
    if len(file_paths) > 3:
        QMessageBox.warning(window, "Limit Reached!", "You can only select up to 3 files.")
        return

    # adding file loop
    for path in file_paths:
        if path not in window.selected_files:
            if len(window.selected_files) < 3:
                window.selected_files.append(path)
                file_list.addItem(os.path.basename(path))
            else:
                print("Maximum of 3 files reached")
                break

    print("FILES BEING PROCESSED:")
    for f in window.selected_files:
        print(f)

    try:
        controller.load_and_process(window.selected_files)
        window.controller = controller

        print("SEGMENTS:")
        print(controller.segment_data["segment_type"].value_counts())

    except Exception as e:
        print(f"Error loading files: {e}")

    # enable navigation buttons
    # disable import button
    # file limit reached
    if len(window.selected_files) >= 3:
        buttonImport.setEnabled(False)
        buttonImport.setStyleSheet("background-color: grey; color: white;")
        buttonPerformance.setEnabled(True)
        buttonBusiness.setEnabled(True)
        buttonForecasting.setEnabled(True)

        buttonPerformance.setStyleSheet("")
        buttonBusiness.setStyleSheet("")
        buttonForecasting.setStyleSheet("")

# remove file
def remove_file():
    selected_items = file_list.selectedItems()

    if not selected_items:
        return

    for item in selected_items:
        filename = item.text()

        for path in window.selected_files:
            if os.path.basename(path) == filename:
                window.selected_files.remove(path)
                break

        file_list.takeItem(file_list.row(item))

    # reprocess remaining files if any
    if window.selected_files:
        try:
            controller.load_and_process(window.selected_files)
            window.controller = controller

        except Exception as e:
            print(f"Error: {e}")

    # reset UI if < 3 files
    if len(window.selected_files) < 3:
        buttonImport.setEnabled(True)
        buttonImport.setStyleSheet("")

        buttonPerformance.setEnabled(False)
        buttonBusiness.setEnabled(False)
        buttonForecasting.setEnabled(False)

        buttonPerformance.setStyleSheet("background-color: grey; color: white;")
        buttonBusiness.setStyleSheet("background-color: grey; color: white;")
        buttonForecasting.setStyleSheet("background-color: grey; color: white;")


# navigation
stack.setCurrentIndex(0)

buttonPerformance.clicked.connect(lambda: stack.setCurrentIndex(1))
buttonBusiness.clicked.connect(lambda: stack.setCurrentIndex(2))
buttonForecasting.clicked.connect(lambda: stack.setCurrentIndex(3))

buttonImport.clicked.connect(import_file)
buttonRemove.clicked.connect(remove_file)

# final setup
main_layout = QVBoxLayout(window)
main_layout.addWidget(stack)

window.show()
app.exec()