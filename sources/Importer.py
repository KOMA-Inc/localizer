from SubmodulesFinder import SubmodulesFinder
from LocalizationFilesReader import LocalizationFilesReader
from PandasManager import PandasManager
from SheetsManager import SheetsManager
from YAMLParser import YAMLParser
from StringsFileWriter import StringsFileWriter
from SheetsNamesCreator import SheetsNamesCreator

class Importer:

    def __init__(self):
        pass

    def import_strings(self, project_path, creds, yaml):
        sheets_url, slack_object = YAMLParser().parse(yaml)
        submodules_list = SubmodulesFinder().submodules(project_path)
        files = LocalizationFilesReader().search(project_path, submodules_list)
        sheets_names = SheetsNamesCreator().create_names(files)
        import_inputs = SheetsManager().importt(sheets_names, creds, sheets_url)
        groups = PandasManager().create_import_groups(import_inputs, files)
        StringsFileWriter().write(groups)