from SubmodulesFinder import SubmodulesFinder
from LocalizationFilesReader import LocalizationFilesReader
from StringsFileReader import StringsFileReader
from GroupsCreator import GroupsCreator
from PandasManager import PandasManager
from SheetsManager import SheetsManager
from YAMLParser import YAMLParser
 
class Exporter:

    def __init__(self):
        pass

    def export_strings(self, project_path, creds, yaml):
        sheets_url, slack_object = YAMLParser().parse(yaml)
        submodules_list = SubmodulesFinder().submodules(project_path)
        files = LocalizationFilesReader().search(project_path, submodules_list)
        entities = StringsFileReader().localization_entities(files)
        groups = GroupsCreator().get_groups(entities)
        inputs = PandasManager().create_export_inputs(groups)
        SheetsManager().export(inputs, creds, sheets_url, slack_object)