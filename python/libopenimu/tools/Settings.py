from PySide6.QtCore import QSettings


class OpenIMUSettings:

    def __init__(self):
        self.settings = QSettings('INTER', 'OpenIMU')

    def add_recent_file(self, file_path: str):
        files = self.get_recent_files()

        # Keep only the latest 5 files
        if len(files) >= 5:
            del files[4:]

        # Is file already there?
        if file_path in files:
            # Yes - move to top of list
            files.insert(0, files.pop(files.index(file_path)))
        else:
            # No - append file
            files.insert(0, file_path)

        self.settings.setValue('recent_files', files)

    def get_recent_files(self) -> list:
        files = self.settings.value('recent_files')
        if not files:
            files = []
        return files

    def remove_recent_file(self, file_path: str):
        files = self.get_recent_files()
        if file_path in files:
            files.remove(file_path)
            self.settings.setValue('recent_files', files)

    @property
    def streamer_data_save_path(self):
        import tempfile
        import os
        return self.settings.value("streamer/savepath", defaultValue=tempfile.gettempdir() + os.sep + "OpenIMU")

    @streamer_data_save_path.setter
    def streamer_data_save_path(self, save_path: str):
        self.settings.setValue('streamer/savepath', save_path)

    @property
    def streamer_port(self):
        return self.settings.value("streamer/port", defaultValue=8118)

    @streamer_port.setter
    def streamer_port(self, port_value: int):
        self.settings.setValue("streamer/port", port_value)

    @property
    def streamer_delete_data_after_transfer(self):
        return self.settings.value("streamer/deletedata", defaultValue=False)

    @streamer_delete_data_after_transfer.setter
    def streamer_delete_data_after_transfer(self, delete: bool):
        self.settings.setValue("streamer/deletedata", delete)

    @property
    def current_language(self) -> str:
        from PySide6.QtCore import QLocale
        language = self.settings.value("language", defaultValue=QLocale.system().language())
        if not isinstance(language, str):
            # No value - set to default language
            if language == QLocale.French:
                language = 'fr'
            elif language == QLocale.English:
                language = 'en'
            else:
                language = 'en'  # Default language for all cases
        return language

    @current_language.setter
    def current_language(self, lang: str):
        self.settings.setValue("language", lang)

    @property
    def data_load_path(self) -> str:
        return self.settings.value("data/loadpath")

    @data_load_path.setter
    def data_load_path(self, path: str):
        self.settings.setValue('data/loadpath', path)

    @property
    def data_save_path(self) -> str:
        return self.settings.value("data/savepath")

    @data_save_path.setter
    def data_save_path(self, path: str):
        self.settings.setValue('data/savepath', path)

    @property
    def database_base_path(self) -> str:
        return self.settings.value("data/databasepath")

    @database_base_path.setter
    def database_base_path(self, path: str):
        self.settings.setValue('data/databasepath', path)

