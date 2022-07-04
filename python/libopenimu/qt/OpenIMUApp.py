from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt, QFile, QLocale, QTranslator, QLibraryInfo, Slot

from libopenimu.tools.Settings import OpenIMUSettings
from libopenimu.qt.StartWindow import StartWindow
from libopenimu.qt.MainWindow import MainWindow

import sys


class OpenIMUApp(QApplication):

    def __init__(self):
        super().__init__()
        self.settings = OpenIMUSettings()
        self.qt_translator = QTranslator()
        self.translator = QTranslator()

        self.start_window = None
        self.main_window = None

        # Set Style
        # style = QStyleFactory.create('Windows')
        # self.setStyle(style)

        # Support high DPI scaling
        # Must be done before starting the app
        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        # Don't quit automatically - because we are using both Start and Main Windows, app can stop early if not set
        self.setQuitOnLastWindowClosed(False)

        # Set stylesheet
        file = QFile(':/stylesheet.qss')
        file.open(QFile.ReadOnly)
        stylesheet = file.readAll()
        stylesheet = str(stylesheet, 'latin1')
        self.setStyleSheet(stylesheet)

        # Load translations
        self.current_lang = self.settings.current_language
        self.set_translations(lang=self.current_lang, force_translate=True)

    def set_translations(self, lang: str, force_translate: bool = False):
        lang = lang.lower()
        lang_changed = lang != self.current_lang

        if lang_changed or force_translate:
            self.current_lang = lang
            if self.current_lang == 'fr':
                locale: QLocale = QLocale(QLocale.French)
            else:  # English or default value
                locale: QLocale = QLocale(QLocale.English)
            QLocale.setDefault(locale)

            # Install Qt Translator for default widgets
            if self.qt_translator.load('qt_' + locale.name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
                self.installTranslator(self.qt_translator)
            else:
                print('Error loading QT translator for default widgets!')

            # Install app specific translator
            if self.translator.load(locale, 'openimu', '_', ':/translations'):
                self.installTranslator(self.translator)
            else:
                print('Error loading app specific translation')

            # Save last settings
            self.settings.current_language = self.current_lang

            # Reload if needed
            if self.start_window:
                self.show_start_window()

    @Slot()
    def start_window_closed(self, result: int):
        if result == QDialog.Rejected:
            sys.exit(0)

        # Show main window
        self.show_main_window(filename=self.start_window.filename, show_importer=self.start_window.importing)
        self.start_window = None

    @Slot()
    def main_window_closing(self):
        if not self.start_window:
            sys.exit(0)

    @Slot()
    def request_show_start_window(self):
        self.show_start_window()
        if self.main_window:
            self.main_window.hide()
            self.main_window = None

    def show_start_window(self):
        if self.start_window:
            self.start_window = None

        self.start_window = StartWindow()
        self.start_window.finished.connect(self.start_window_closed)
        self.start_window.request_language_change.connect(self.set_translations)

        self.start_window.show()

    def show_main_window(self, filename: str, show_importer: bool = False):
        if self.main_window:
            self.main_window = None

        self.main_window = MainWindow(filename=filename)
        self.main_window.aboutToClose.connect(self.main_window_closing)
        self.main_window.showStartWindow.connect(self.request_show_start_window)
        self.main_window.showMaximized()
        if show_importer:
            self.main_window.import_requested()

    def exec(self) -> int:
        #  Show start window
        self.show_start_window()

        # if start_window.exec() == QDialog.Rejected:
        #     # User closed the dialog - exits!
        #     sys.exit(0)

        return QApplication.exec()
