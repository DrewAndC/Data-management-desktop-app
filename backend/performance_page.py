from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import calendar

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates


class PerformancePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle('RoastWorks Sales Performance Dashboard')
        # initial graph size
        self.window_size = 6

        # Track selected month
        self.month_index = -1

        # main layout
        main_layout = QHBoxLayout(self)

        # left side
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(150)

        logo_label = QLabel()
        pixmap = QPixmap('backend/icons/Logo2.png').scaled(200, 200)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttonMain = QPushButton("Home")
        buttonPerformance = QPushButton("Sales")
        buttonBusiness = QPushButton("Business")
        buttonForecasting = QPushButton("Forecasting")

        buttonMain.clicked.connect(lambda: stack.setCurrentIndex(0))
        buttonPerformance.clicked.connect(lambda: stack.setCurrentIndex(1))
        buttonBusiness.clicked.connect(lambda: stack.setCurrentIndex(2))
        buttonForecasting.clicked.connect(lambda: stack.setCurrentIndex(3))

        left_layout.addWidget(logo_label)
        left_layout.addSpacing(100)
        left_layout.addWidget(buttonMain)
        left_layout.addWidget(buttonPerformance)
        left_layout.addWidget(buttonBusiness)
        left_layout.addWidget(buttonForecasting)
        left_layout.addStretch()

        # right side
        right_layout = QVBoxLayout()

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # top buttons
        button_row = QHBoxLayout()

        buttonRevenue = QPushButton("Revenue")
        buttonProfit = QPushButton("Profit")
        buttonGross = QPushButton("Gross")
        buttonUDC = QPushButton("UDC")
        buttonACC = QPushButton("ACC")
        buttonMM = QPushButton("MnMRG")
        
        buttonPrevious = QPushButton("Previous")
        buttonNext = QPushButton("Next")

        button_row.addWidget(buttonRevenue)
        button_row.addWidget(buttonProfit)
        button_row.addWidget(buttonGross)
        button_row.addWidget(buttonUDC)
        button_row.addWidget(buttonACC)
        button_row.addWidget(buttonMM)
        button_row.addStretch()
        button_row.addWidget(buttonPrevious)
        button_row.addWidget(buttonNext)

        # styling name of buttons
        buttonMain.setObjectName("greyButton")
        buttonBusiness.setObjectName("greyButton")
        buttonForecasting.setObjectName("greyButton")
        buttonPrevious.setObjectName("greyButton")

        # connect buttons to metric selection
        buttonRevenue.clicked.connect(lambda: self.update_metric("revenue"))
        buttonProfit.clicked.connect(lambda: self.update_metric("profit"))
        buttonGross.clicked.connect(lambda: self.update_metric("margin"))
        buttonUDC.clicked.connect(lambda: self.update_metric("unique_domestic_customers"))
        buttonACC.clicked.connect(lambda: self.update_metric("active_commercial_customers"))
        buttonMM.clicked.connect(lambda: self.update_metric("revenue_growth"))
        # previous and Next buttons
        buttonPrevious.clicked.connect(lambda: self.show_previous_month())
        buttonNext.clicked.connect(lambda: self.show_next_month())

        # matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # main content
        right_layout.addStretch()
        content_widget.setStyleSheet("""background-color: #FFFFFF;
                                     border-radius: 20px""")
        content_widget.setFixedHeight(500)
        
        # HBOX for KPI and graph
        graph_kpi_layout = QHBoxLayout()
        
        # KPI (left side)
        kpi_layout = QVBoxLayout()
        self.kpi_month_name_title = QLabel("Select a month")
        self.kpi_title = QLabel("Select a metric")
        self.kpi_current = QLabel("null")
        self.kpi_month_title = QLabel("This month")
        self.kpi_previous = QLabel("null")
        self.kpi_month_title2 = QLabel("Last month")
        self.kpi_change = QLabel("x.xx%")
        self.kpi_change_title = QLabel("Change")

        kpi_layout.addWidget(self.kpi_month_name_title)
        kpi_layout.addSpacing(20)
        kpi_layout.addWidget(self.kpi_title)
        kpi_layout.addSpacing(10)
        kpi_layout.addWidget(self.kpi_current)
        kpi_layout.addWidget(self.kpi_month_title)
        kpi_layout.addSpacing(10)
        kpi_layout.addWidget(self.kpi_previous)
        kpi_layout.addWidget(self.kpi_month_title2)
        kpi_layout.addSpacing(10)
        kpi_layout.addWidget(self.kpi_change)
        kpi_layout.addWidget(self.kpi_change_title)
        kpi_layout.addStretch()

        kpi_widget = QWidget()
        kpi_widget.setLayout(kpi_layout)
        kpi_widget.setFixedWidth(200)

        # add KPI layout to graph_kpi_layout
        graph_kpi_layout.addWidget(kpi_widget)

        # graph (right side)
        graph_kpi_layout.addWidget(self.canvas, 1)

        content_layout.addLayout(graph_kpi_layout)

        # slider content
        slider_row = QHBoxLayout()

        self.window_slider = QSlider(Qt.Orientation.Horizontal)
        self.window_label = QLabel("Window Size: ")
        self.window_label_display = QLabel("6")

        # configure slider range
        self.window_slider.setMinimum(3) # 6 months
        self.window_slider.setMaximum(18) # 36 months
        self.window_slider.setValue(3) # initial of 6 months

        self.window_slider.setTickInterval(1)
        self.window_slider.setSingleStep(1)

        slider_row.addWidget(self.window_slider)
        slider_row.addWidget(self.window_label)
        slider_row.addWidget(self.window_label_display)
        slider_row.addStretch()

        # connect slider to window size function
        self.window_slider.valueChanged.connect(self.update_window_size)

        # dropdown box content
        dropdown_row = QHBoxLayout()
        self.year_dropdown = QComboBox()
        self.month_dropdown = QComboBox()

        dropdown_row.addWidget(self.year_dropdown)
        dropdown_row.addWidget(self.month_dropdown)
        dropdown_row.addStretch()

        # add to right layout
        right_layout.addLayout(button_row)
        right_layout.addWidget(content_widget)
        right_layout.addLayout(slider_row)
        right_layout.addLayout(dropdown_row)
        right_layout.addStretch()

        # connect boxes to update function
        self.year_dropdown.currentTextChanged.connect(self.update_new_date)
        self.month_dropdown.currentTextChanged.connect(self.update_new_date)

        # wrap in widget for background color
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # add content to main layout    
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget, 1)

    # plot data function
    def plot_data(self):
        main_window = self.stack.parent()

        full_df = main_window.controller.monthly_data.copy()
        full_df = full_df.sort_values('month').reset_index(drop=True)

        n = len(full_df)

        # current index
        current_index = n + self.month_index if self.month_index < 0 else self.month_index

        # clamp index
        current_index = max(0, min(current_index, n - 1))

        # plot window size
        window = self.window_size
        half_window = window // 2

        start = current_index - half_window
        end = current_index + half_window

        # clamp edges
        if start < 0 :
            start = 0
            end = window
        
        if end > n:
            end = n
            start = n - window

        df = full_df.iloc[start:end].copy()

        # draw plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # convert month to datetime
        df['month'] = pd.to_datetime(df['month'])

        # plot lines using real dates
        ax.plot(df["month"], df['revenue'], marker='o', label='Revenue')
        ax.plot(df["month"], df['cost'], marker='o', label='Cost')
        ax.plot(df["month"], df['profit'], marker='o', label='Profit')

        # format x-axis (clean dates)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # auto rotate nicely
        self.figure.autofmt_xdate()

        # vertical line using DATE (not index)
        position = current_index - start
        current_date = df["month"].iloc[position]
        ax.axvline(x=current_date, linestyle='--', linewidth=1)

        ax.legend()

        self.canvas.draw()

    # show event to refresh data when page is shown
    def showEvent(self, event):
        super().showEvent(event)

        # reset to latest month and default to revenue kpi
        self.month_index = -1
        self.current_metric = "revenue"

        self.plot_data()   
        self.refresh_kpi()
        self.populate_dropdown()

    # update metric display function
    def update_metric(self, metric):
        self.current_metric = metric
        self.refresh_kpi()
        
        
# show previous month data
    def show_previous_month(self):
        main_window = self.stack.parent()
        df = main_window.controller.monthly_data.copy()

        if self.month_index > -len(df):
            self.month_index -= 1
        
        self.refresh_kpi()
        self.plot_data()

    def show_next_month(self):
        if self.month_index < -1:
            self.month_index += 1
        
        self.refresh_kpi()
        self.plot_data()

    def refresh_kpi(self):
        main_window = self.stack.parent()

        # copy dataframe
        df = main_window.controller.monthly_data.copy()

        # get latest month data
        df = df.sort_values('month')
        current = df.iloc[self.month_index]

        metric = getattr(self, "current_metric", "revenue")

        # get specific metric values
        current_value = current[metric]
        previous_value = current[f"{metric}_prev"]
        change_value = current[f"{metric}_change"]

        # map metric to display name
        metric_names = {
            "revenue": "Total Revenue",
            "profit": "Total Profit",
            "margin": "Gross Margin (%)",
            "unique_domestic_customers": "Unique Domestic Customers",
            "active_commercial_customers": "Active Commercial Customers",
            "revenue_growth": "Month on Month Revenue Growth (%)"
        }

        # month display formatting
        month_string = str(current['month'])
        year, month = month_string.split("-")

        month_name = calendar.month_name[int(month)]

        # update kpi labels
        self.kpi_month_name_title.setText(f"{month_name} {year}")
        self.kpi_title.setText(metric_names.get(metric, "Metric"))

        if "customers" in metric:
            self.kpi_current.setText(f"{int(current_value):,}")
            self.kpi_previous.setText(f"{int(previous_value):,}")
            self.kpi_change.setText(f"{int(change_value):+}")
        elif "margin" in metric or "growth" in metric:
            self.kpi_current.setText(f"{current_value:.2f}%")
            self.kpi_previous.setText(f"{previous_value:.2f}%")
            self.kpi_change.setText(f"{change_value:+.2f}%")
        else:
            self.kpi_current.setText(f"${current_value:,.2f}")
            self.kpi_previous.setText(f"${previous_value:,.2f}")
            self.kpi_change.setText(f"${change_value:+,.2f}")

        # change color of change label
        if change_value > 0:
            self.kpi_change.setStyleSheet("color: green;")
        elif change_value < 0:
            self.kpi_change.setStyleSheet("color: red;")
        else:
            self.kpi_change.setStyleSheet("color: black;")

    def update_window_size(self, value):
        # increment window size by 2 
        self.window_size = value * 2
        # display new window size
        self.window_label_display.setText(str(self.window_size))
        # update graph to window size
        self.plot_data()

    def populate_dropdown(self):
        main_window = self.stack.parent()

        df = main_window.controller.monthly_data.copy()
        df = df.sort_values('month')

        # get yeah and month from dataframe
        df['year'] = df['month'].astype(str).str[:4]
        df['month_num'] = df['month'].astype(str).str[5:7]

        # sort to only unique items
        years = sorted(df['year'].unique())
        months = sorted(df['month_num'].unique())

        # clears dropdown boxes to empty
        self.year_dropdown.clear()
        self.month_dropdown.clear()

        # formatting of months to string type
        month_names = [calendar.month_name[int(m)] for m in months]

        self.year_dropdown.addItems(years)
        self.month_dropdown.addItems(month_names)

    def update_new_date(self):
        main_window = self.stack.parent()

        df = main_window.controller.monthly_data.copy()
        df = df.sort_values('month').reset_index(drop=True)

        selected_year = self.year_dropdown.currentText()
        selected_month = self.month_dropdown.currentText()

        month_number = list(calendar.month_name).index(selected_month)
        month_new = f"{month_number:02d}"

        # format to original format
        target = f"{selected_year}-{month_new}"

          # find index
        matches = df[df['month'].astype(str) == target]

        if not matches.empty:
            index = matches.index[0]

            # convert to negative index system
            self.month_index = index - len(df)

            self.refresh_kpi()
            self.plot_data()
