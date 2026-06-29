from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import calendar

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ForecastingPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle('RoastWorks Forecasting Dashboard')
        # initial graph size
        self.train_window = 6
        # initial horizon size
        self.horizon = 3
        # initial error metric
        self.error_metric = "mae"

        # track selected month
        self.month_index = -1

        # initial metric
        self.current_metric = "revenue"

        # global sale type
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

        buttonRevenue = QPushButton("Revenue")
        buttonCost = QPushButton("Cost")
        buttonMargin = QPushButton("Margin")
        buttonErrorMetric = QPushButton("MAE")
        
        button_row.addWidget(buttonRevenue)
        button_row.addWidget(buttonCost)
        button_row.addWidget(buttonMargin)
        button_row.addStretch()
        button_row.addWidget(buttonErrorMetric)

        # styling name of buttons
        buttonMain.setObjectName("greyButton")
        buttonPerformance.setObjectName("greyButton")
        buttonBusiness.setObjectName("greyButton")
        buttonErrorMetric.setObjectName("greyButton")

        # connect buttons to metric selection
        buttonRevenue.clicked.connect(lambda: self.set_metric("revenue"))
        buttonCost.clicked.connect(lambda: self.set_metric("cost"))
        buttonMargin.clicked.connect(lambda: self.set_metric("margin"))
        # connect error metric button to toggle function
        buttonErrorMetric.clicked.connect(self.toggle_error_metric)
        # store reference
        self.error_button = buttonErrorMetric

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
        # forecast KPI block
        self.kpi_title = QLabel("Forecasting Model")

        self.kpi_error_value = QLabel("+- XXXX")
        self.kpi_error_label = QLabel("Error Metric")

        self.kpi_actual_value = QLabel("$0")
        self.kpi_actual_label = QLabel("Last Month")

        self.kpi_change_value = QLabel("0.0%")
        self.kpi_change_label = QLabel("Change")
        
        kpi_layout = QVBoxLayout()

        kpi_layout.addWidget(self.kpi_title)
        kpi_layout.addSpacing(20)
        kpi_layout.addWidget(self.kpi_error_value)
        kpi_layout.addWidget(self.kpi_error_label)
        kpi_layout.addSpacing(15)
        kpi_layout.addWidget(self.kpi_actual_value)
        kpi_layout.addWidget(self.kpi_actual_label)
        kpi_layout.addSpacing(15)
        kpi_layout.addWidget(self.kpi_change_value)
        kpi_layout.addWidget(self.kpi_change_label)
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

        # training window slider content
        self.train_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_label = QLabel("Training window (months): ")
        self.size_label_display = QLabel("3")

        # configure slider range
        self.train_slider.setMinimum(3) # 6 months
        self.train_slider.setMaximum(18) # 36 months
        self.train_slider.setValue(3) # initial of 6 months

        self.train_slider.setTickInterval(1)
        self.train_slider.setSingleStep(1)

        # horizon slider content
        self.horizon_slider = QSlider(Qt.Orientation.Horizontal)
        self.horizon_label = QLabel("Forecast horizon (months): ")
        self.horizon_label_display = QLabel("3")

        # configure range
        self.horizon_slider.setMinimum(3)
        self.horizon_slider.setMaximum(24)
        self.horizon_slider.setValue(3)
    
        self.horizon_slider.setTickInterval(1)
        self.horizon_slider.setSingleStep(1)

        slider_row.addWidget(self.train_slider)
        slider_row.addWidget(self.size_label)
        slider_row.addWidget(self.size_label_display)
        slider_row.addStretch()
        slider_row.addWidget(self.horizon_slider)
        slider_row.addWidget(self.horizon_label)
        slider_row.addWidget(self.horizon_label_display)

        # connect slider to training window size function
        self.train_slider.valueChanged.connect(self.update_forecast_size)
        self.size_label_display.setText(str(self.train_slider.value()))

        # connect horizon slider to update function
        self.horizon_slider.valueChanged.connect(self.update_horizon)

        # dropdown box and checkbox content
        dropdown_row = QHBoxLayout()
        self.checkbox_naive = QCheckBox("Naive")
        self.checkbox_moving_average = QCheckBox("Moving Avg")
        self.checkbox_arima = QCheckBox("Arima")

        self.checkbox_naive.setChecked(True)

        dropdown_row.addStretch()
        dropdown_row.addWidget(self.checkbox_naive)
        dropdown_row.addWidget(self.checkbox_moving_average)
        dropdown_row.addWidget(self.checkbox_arima)

        # connect checkboxes to graph
        self.checkbox_naive.stateChanged.connect(self.plot_data)
        self.checkbox_moving_average.stateChanged.connect(self.plot_data)
        self.checkbox_arima.stateChanged.connect(self.plot_data)

        # add to right layout
        right_layout.addLayout(button_row)
        right_layout.addWidget(content_widget)
        right_layout.addLayout(slider_row)
        right_layout.addLayout(dropdown_row)
        right_layout.addStretch()

        # wrap in widget for background color
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # add content to main layout    
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget, 1)

    # plot data function
    def plot_data(self):
        main_window = self.stack.parent()
        controller = main_window.controller

        # forecast data moves with slider
        data = controller.forecast(horizon=self.horizon, train_window=self.train_window)

        # get chosen metric
        metric = self.current_metric
        result = data["metrics"][metric]

        actual = result["actual"]
        models = result["models"]

        x_actual = list(range(len(actual)))
        x_prediction = list(range(len(actual), len(actual) + len(data["months"])))

        selected_models = []

        # checks which forecasting model checkbox is selected and append to selected list
        if self.checkbox_naive.isChecked():
            selected_models.append("naive")

        if self.checkbox_moving_average.isChecked():
            selected_models.append("moving_average")

        if self.checkbox_arima.isChecked():
            selected_models.append("arima")

        if not selected_models:
            return

        # plot forecasting models
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # plot actual line
        ax.plot(x_actual, actual, marker='o', linewidth=2, label="Actual")

        # loop through selected_models and plot model/s
        for m in selected_models:
            prediction = models[m]["predictions"]

            ax.plot(x_prediction, prediction, marker='o', linestyle='--', linewidth=2, label=f"{m.replace('_', ' ').title()} Forecast")
        
        # vertical line where forecast starts
        ax.axvline(x=len(actual)-1, linestyle='--')
        
        # title
        ax.set_title(f"{metric.capitalize()} Forecast Comparison")
        ax.legend()

        self.canvas.draw()
        self.refresh_kpi()


    # show event to refresh data when page is shown
    def showEvent(self, event):
        super().showEvent(event)

        # reset to latest month and default to revenue kpi
        self.month_index = -1

        self.plot_data()   
        self.refresh_kpi()

    def refresh_kpi(self):
        main_window = self.stack.parent()
        controller = main_window.controller

        df = controller.monthly_data.copy()
        df = df.sort_values('month').reset_index(drop=True)

        # get most recent month
        current = df.iloc[-1]

        # get previous month
        previous = df.iloc[-2] if len(df) > 1 else current

        # get data of metric for current and previous
        metric = self.current_metric
        current_value = current[metric]
        previous_value = previous[metric]

        try:
            data = controller.forecast(
                horizon=self.horizon,
                train_window=self.train_window
            )

            result = data["metrics"][metric]

            best_model = result["best_model"]
            error = result["models"][best_model][self.error_metric]

            # first predicted value
            forecast_value = result["best_predictions"][0]

        except Exception:
            # fallback if forecasting fails
            best_model = "N/A"
            error = 0
            forecast_value = 0

        self.kpi_title.setText(f"Best Model: {best_model.replace('_',' ').title()}")

        # error (MAE)
        self.kpi_error_value.setText(f"± {error:,.2f}")
        self.kpi_error_label.setText(f"Error {self.error_metric.upper()}")

        # latest actual value
        self.kpi_actual_value.setText(f"${current_value:,.2f}")
        self.kpi_actual_label.setText("Latest Actual")

        # forecast value next
        self.kpi_change_value.setText(f"${forecast_value:,.2f}")
        self.kpi_change_label.setText("Next Forecast")

        # colour change based of change
        if forecast_value > current_value:
            self.kpi_change_value.setStyleSheet("color: green;")
        elif forecast_value < current_value:
            self.kpi_change_value.setStyleSheet("color: red;")
        else:
            self.kpi_change_value.setStyleSheet("color: black;")

    def set_metric(self, metric):
        self.current_metric = metric
        self.plot_data()

    def update_forecast_size(self, value):
        # minimum of 3
        self.train_window = max(3, value)

        # update label
        self.size_label_display.setText(str(self.train_window))

        # update graph
        self.plot_data()

    def update_horizon(self, value):
        self.horizon = max(3, value)
        self.horizon_label_display.setText(str(self.horizon))
        self.plot_data()

    # error metric toggle function
    def toggle_error_metric(self):
        # switch between error metrics depending on reference
        if self.error_metric == "mae":
            self.error_metric = "mse"
            self.error_button.setText("MSE")
        else:
            self.error_metric = "mae"
            self.error_button.setText("MAE")

        self.refresh_kpi()