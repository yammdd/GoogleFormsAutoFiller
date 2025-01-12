import threading
from PyQt6 import QtCore, QtGui, QtWidgets
from Survey import Survey

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("AutoFiller")
        MainWindow.setFixedSize(760, 470)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self._setup_fonts()
        self.centralwidget.setFont(self.default_font)
        self.centralwidget.setObjectName("centralwidget")

        self._setup_main_label()
        self._setup_group_box()
        self._setup_list_widget()
        self._setup_menu_and_status_bar(MainWindow)

        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.survey = None
        self.survey_thread = None

    def _setup_fonts(self):
        self.default_font = QtGui.QFont("Roboto", 12, QtGui.QFont.Weight.Bold)
        self.medium_font = QtGui.QFont("Roboto Medium", 14)
        self.light_font = QtGui.QFont("Roboto Light", 12)
        self.thin_font = QtGui.QFont("Roboto Thin", 10)

    def _setup_main_label(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 10, 400, 30))
        label_font = QtGui.QFont("Roboto Medium", 20, italic=True)
        self.label.setFont(label_font)
        self.label.setObjectName("label")

    def _setup_group_box(self):
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 40, 441, 381))
        self.groupBox.setFont(self.medium_font)
        self.groupBox.setObjectName("groupBox")

        self._setup_group_box_content()

    def _setup_group_box_content(self):
        self._setup_url_input()
        self._setup_textfields()
        self._setup_choices_input()
        self._setup_buttons()
        self._setup_labels()
        self._setup_number_input()

    def _setup_url_input(self):
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 47, 21))
        self.label_2.setFont(self.light_font)
        self.label_2.setObjectName("label_2")

        self.get_url = QtWidgets.QLineEdit(self.groupBox)
        self.get_url.setGeometry(QtCore.QRect(70, 30, 280, 25))
        self.get_url.setObjectName("get_url")

    def _setup_textfields(self):
        self.input_textfields = QtWidgets.QTextEdit(self.groupBox)
        self.input_textfields.setGeometry(QtCore.QRect(70, 90, 280, 70))
        self.input_textfields.setObjectName("input_textfields")

    def _setup_choices_input(self):
        self.input_choices = QtWidgets.QTextEdit(self.groupBox)
        self.input_choices.setGeometry(QtCore.QRect(70, 210, 280, 160))
        self.input_choices.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.input_choices.setObjectName("input_choices")

    def _setup_number_input(self):
        self.label_quantity = QtWidgets.QLabel(self.groupBox)
        self.label_quantity.setGeometry(QtCore.QRect(360, 90, 80, 25))
        self.label_quantity.setFont(QtGui.QFont("Roboto Light", 8))
        self.label_quantity.setObjectName("label_quantity")

        self.input_quantity = QtWidgets.QSpinBox(self.groupBox)
        self.input_quantity.setGeometry(QtCore.QRect(350, 120, 20, 25))
        self.input_quantity.setMinimum(1)
        self.input_quantity.setMaximum(1000)
        self.input_quantity.setObjectName("input_quantity")

    def _setup_buttons(self):
        self.start_button = QtWidgets.QPushButton(self.groupBox)
        self.start_button.setGeometry(QtCore.QRect(360, 30, 75, 23))
        self.start_button.setFont(self.thin_font)
        self.start_button.setObjectName("start_button")

        self.stop_button = QtWidgets.QPushButton(self.groupBox)
        self.stop_button.setGeometry(QtCore.QRect(360, 60, 75, 23))
        self.stop_button.setFont(self.thin_font)
        self.stop_button.setObjectName("stop_button")

    def _setup_labels(self):
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(70, 60, 190, 20))
        self.label_3.setFont(QtGui.QFont("Roboto Light", 7))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(70, 160, 291, 41))
        self.label_4.setFont(QtGui.QFont("Roboto Light", 7))
        self.label_4.setObjectName("label_4")

    def _setup_list_widget(self):
        self.text_display = QtWidgets.QListWidget(self.centralwidget)
        self.text_display.setGeometry(QtCore.QRect(460, 50, 290, 371))
        self.text_display.setObjectName("text_display")

    def _setup_menu_and_status_bar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TỰ ĐỘNG ĐIỀN GOOGLE FORM"))
        self.groupBox.setTitle(_translate("MainWindow", "Dữ liệu"))
        self.label_2.setText(_translate("MainWindow", "URL:"))
        self.label_quantity.setText(_translate("MainWindow", "Số lượng:"))
        self.input_choices.setHtml(_translate("MainWindow", "<p style=\"margin:0;\"><br></p>"))
        self.input_textfields.setHtml(_translate("MainWindow", "<p style=\"margin:0;\"><br></p>"))
        self.start_button.setText(_translate("MainWindow", "Bắt đầu"))
        self.stop_button.setText(_translate("MainWindow", "Dừng"))
        self.label_3.setText(_translate("MainWindow", "Nhập văn bản mong muốn (không bắt buộc):"))
        self.label_4.setText(_translate("MainWindow", "Nhập dữ liệu đáp án trắc nghiệm mong muốn, có dạng:\n"
                                                      "Đáp án 1, Đáp án 2, ..."))

    def on_start_button_clicked(self):
        """Handle start button click."""
        self.text_display.clear()
        url = self.get_url.text()
        responses = self.input_quantity.value()
        choice_answers = self.input_choices.toPlainText().split(", ")
        choice_answers[-1] = choice_answers[-1].replace("\n", "")
        if choice_answers == [""]:
            choice_answers = []
        input_text = self.input_textfields.toPlainText()
        if input_text == "\n":
            input_text = ""

        self.survey = Survey("../data/chromedriver.exe", url, responses, ui=self)

        self.survey_thread = threading.Thread(target=self.survey.start, args=(choice_answers, input_text), daemon=True)
        self.survey_thread.start()
        self.add_item_to_list_widget("Chương trình đã bắt đầu.")

    def on_stop_button_clicked(self):
        """Handle stop button click."""
        if self.survey:
            self.survey.quit_anyway()
            self.add_item_to_list_widget("Dừng, đang xử lý mẫu cuối.")

    def add_item_to_list_widget(self, item):
        self.text_display.addItem(item)
