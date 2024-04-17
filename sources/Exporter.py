from SubmodulesFinder import SubmodulesFinder
from LocalizationFilesReader import LocalizationFilesReader
from StringsFileReader import StringsFileReader
from GroupsCreator import GroupsCreator
 
class Exporter:

    def __init__(self):
        pass

    def export_strings(self, project_path):
        submodules_list = SubmodulesFinder().submodules(project_path)
        files = LocalizationFilesReader().search(project_path, submodules_list)
        entities = StringsFileReader().localization_entities(files)
        groups = GroupsCreator().get_groups(entities)
