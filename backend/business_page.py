from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import calendar

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates


class BusinessPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle('RoastWorks Business Performance Dashboard')
        # initial graph size
        self.window_size = 6

        # Track selected month
        self.month_index = -1

        # Global sale type
        self.sale_type = "commercial"

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

        buttonCommercial = QPushButton("Commercial")
        buttonDomestic = QPushButton("Domestic")
        buttonCafe = QPushButton("Cafe")
        
        buttonPrevious = QPushButton("Previous")
        buttonNext = QPushButton("Next")

        button_row.addWidget(buttonCommercial)
        button_row.addWidget(buttonDomestic)
        button_row.addWidget(buttonCafe)
        button_row.addStretch()
        button_row.addWidget(buttonPrevious)
        button_row.addWidget(buttonNext)

        # styling name of buttons
        buttonMain.setObjectName("greyButton")
        buttonPerformance.setObjectName("greyButton")
        buttonForecasting.setObjectName("greyButton")
        buttonPrevious.setObjectName("greyButton")

        # connect buttons to metric selection
        buttonCommercial.clicked.connect(lambda: self.set_sale_type("commercial"))
        buttonDomestic.clicked.connect(lambda: self.set_sale_type("domestic"))
        buttonCafe.clicked.connect(lambda: self.set_sale_type("cafe"))
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

        # profit labels
        self.kpi_p_title = QLabel("")
        self.kpi_p_current = QLabel("null")
        self.kpi_p_month_title = QLabel("This month")
        self.kpi_p_previous = QLabel("null")
        self.kpi_p_month_title2 = QLabel("Last month")
        self.kpi_p_change = QLabel("x.xx%")
        self.kpi_p_change_title = QLabel("Change")

        # cost labels
        self.kpi_c_title = QLabel("")
        self.kpi_c_current = QLabel("null")
        self.kpi_c_month_title = QLabel("This month")
        self.kpi_c_previous = QLabel("null")
        self.kpi_c_month_title2 = QLabel("Last month")
        self.kpi_c_change = QLabel("x.xx%")
        self.kpi_c_change_title = QLabel("Change")

        # revenue labels
        self.kpi_r_title = QLabel("")
        self.kpi_r_current = QLabel("null")
        self.kpi_r_month_title = QLabel("This month")
        self.kpi_r_previous = QLabel("null")
        self.kpi_r_month_title2 = QLabel("Last month")
        self.kpi_r_change = QLabel("x.xx%")
        self.kpi_r_change_title = QLabel("Change")
        

        kpi_layout.addWidget(self.kpi_month_name_title)
        kpi_layout.addSpacing(20)

        # profit label add to layout
        kpi_layout.addWidget(self.kpi_p_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_p_current)
        kpi_layout.addWidget(self.kpi_p_month_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_p_previous)
        kpi_layout.addWidget(self.kpi_p_month_title2)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_p_change)
        kpi_layout.addWidget(self.kpi_p_change_title)
        kpi_layout.addSpacing(10)

        # cost label add to layout
        kpi_layout.addWidget(self.kpi_c_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_c_current)
        kpi_layout.addWidget(self.kpi_c_month_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_c_previous)
        kpi_layout.addWidget(self.kpi_c_month_title2)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_c_change)
        kpi_layout.addWidget(self.kpi_c_change_title)
        kpi_layout.addSpacing(10)

        # revenue label add to layout
        kpi_layout.addWidget(self.kpi_r_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_r_current)
        kpi_layout.addWidget(self.kpi_r_month_title)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_r_previous)
        kpi_layout.addWidget(self.kpi_r_month_title2)
        kpi_layout.addSpacing(5)
        kpi_layout.addWidget(self.kpi_r_change)
        kpi_layout.addWidget(self.kpi_r_change_title)
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

        # dropdown box and checkbox content
        dropdown_row = QHBoxLayout()
        self.year_dropdown = QComboBox()
        self.month_dropdown = QComboBox()
        self.checkbox_commercial = QCheckBox("Commercial")
        self.checkbox_domestic = QCheckBox("Domestic")
        self.checkbox_cafe = QCheckBox("Cafe")

        self.checkbox_commercial.setChecked(True)

        dropdown_row.addWidget(self.year_dropdown)
        dropdown_row.addWidget(self.month_dropdown)
        dropdown_row.addStretch()
        dropdown_row.addWidget(self.checkbox_commercial)
        dropdown_row.addWidget(self.checkbox_domestic)
        dropdown_row.addWidget(self.checkbox_cafe)

        # connect checkboxes to graph
        self.checkbox_commercial.stateChanged.connect(self.plot_data)
        self.checkbox_domestic.stateChanged.connect(self.plot_data)
        self.checkbox_cafe.stateChanged.connect(self.plot_data)

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

        full_df = main_window.controller.segment_data.copy()
        full_df = full_df.sort_values('month').reset_index(drop=True)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        selected_segments = []

        # check which sale type is selected from checkboxes
        if self.checkbox_commercial.isChecked():
            selected_segments.append("commercial")

        if self.checkbox_domestic.isChecked():
            selected_segments.append("domestic")

        if self.checkbox_cafe.isChecked():
            selected_segments.append("cafe")

        if not selected_segments:
            return
        
        # reference of window size and position
        reference_df = full_df[full_df["segment_type"] == selected_segments[0]]
        reference_df = reference_df.sort_values('month').reset_index(drop=True)
        
        n = len(reference_df)
        current_index = n + self.month_index if self.month_index < 0 else self.month_index
        current_index = max(0, min(current_index, n - 1))

        window = self.window_size
        half_window = window // 2
        start = current_index - half_window
        end = current_index + half_window + 1

        # clamp edges
        if start < 0:
            start = 0
            end = min(window, n)

        if end > n:
            end = n
            start = max(0, n - window)

        # position of vertical line
        position = current_index - start

        # plot each sale type that is selected, loops through list
        for s in selected_segments:
            s_df = full_df[full_df["segment_type"] == s]
            s_df = s_df.sort_values('month').reset_index(drop=True)

            df = s_df.iloc[start:end].copy()
            df['month'] = pd.to_datetime(df['month'])

            ax.plot(df["month"], df['revenue'], marker='o',
                    label=f"{s.capitalize()} Revenue")

            ax.plot(df["month"], df['profit'], linestyle='--', marker='o',
                    label=f"{s.capitalize()} Profit")

            ax.plot(df["month"], df['profit_change'], linestyle=':', marker='o',
                    label=f"{s.capitalize()} Growth")

        # vertical line (date-based)
        ref_window = reference_df.iloc[start:end].copy()
        ref_window['month'] = pd.to_datetime(ref_window['month'])
        current_date = ref_window["month"].iloc[position]

        ax.axvline(x=current_date, linestyle='--', linewidth=1)

        # clean axis
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        self.figure.autofmt_xdate()

        ax.set_title("Revenue, Profit & Growth by Sale Type")
        ax.legend()
        self.canvas.draw()

    # show event to refresh data when page is shown
    def showEvent(self, event):
        super().showEvent(event)

        # reset to latest month and default to revenue kpi
        self.month_index = -1

        self.plot_data()   
        self.refresh_kpi()
        self.populate_dropdown()
        
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
        df = main_window.controller.segment_data.copy()
        df = df[df["segment_type"] == self.sale_type]
        df = df.sort_values('month').reset_index(drop=True)

        current = df.iloc[self.month_index]

        # get profit metric values
        current_profit = current["profit"]
        previous_profit = current[f"profit_prev"]
        change_profit = current[f"profit_change"]

        # get cost metric values
        current_cost = current["cost"]
        previous_cost = current[f"cost_prev"]
        change_cost = current[f"cost_change"]

        # get revenue metric values
        current_revenue = current["revenue"]
        previous_revenue = current[f"revenue_prev"]
        change_revenue = current[f"revenue_change"]

        # month display formatting
        month_string = str(current['month'])
        year, month = month_string.split("-")
        month_name = calendar.month_name[int(month)]

        # update kpi labels
        self.kpi_month_name_title.setText(f"{month_name} {year}")

        # update profit labels
        self.kpi_p_title.setText(f"{self.sale_type.capitalize()} Gross Profit")
        self.kpi_p_current.setText(f"${current_profit:,.2f}")
        self.kpi_p_previous.setText(f"${previous_profit:,.2f}")
        self.kpi_p_change.setText(f"${change_profit:+,.2f}")

        # update cost labels
        self.kpi_c_title.setText(f"{self.sale_type.capitalize()} Cost")
        self.kpi_c_current.setText(f"${current_cost:,.2f}")
        self.kpi_c_previous.setText(f"${previous_cost:,.2f}")
        self.kpi_c_change.setText(f"${change_cost:+,.2f}")

        # update revenue labels
        self.kpi_r_title.setText(f"{self.sale_type.capitalize()} Revenue")
        self.kpi_r_current.setText(f"${current_revenue:,.2f}")
        self.kpi_r_previous.setText(f"${previous_revenue:,.2f}")
        self.kpi_r_change.setText(f"${change_revenue:+,.2f}")

        def set_color(label, value):
            if value > 0:
                label.setStyleSheet("color: green;")
            elif value < 0:
                label.setStyleSheet("color: red;")
            else:
                label.setStyleSheet("color: black;")

        set_color(self.kpi_p_change, change_profit)
        set_color(self.kpi_c_change, change_cost)
        set_color(self.kpi_r_change, change_revenue)

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

    def set_sale_type(self, sale_type):
        self.sale_type = sale_type
        self.plot_data()
        self.refresh_kpi()