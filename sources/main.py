import os
from LocalizationFilesReader import LocalizationFilesReader
from ArgumentParser import ArgumentParser
from Exporter import Exporter
from Importer import Importer

def search(project_directory, escaping_paths):
    folder = os.path.dirname(project_directory)
    LocalizationFilesReader().search(folder, escaping_paths)

def import_data(project_path, creds_path, yaml):
   Importer().import_strings(project_path, creds_path, yaml)

def export_data(project_path, creds_path, yaml):
    Exporter().export_strings(project_path, creds_path, yaml)

def main():
    (command, project, config, yaml) = ArgumentParser().start()

    if command == "import":
        import_data(project, config, yaml)
    elif command == "export":
        export_data(project, config, yaml)

if __name__ == "__main__":
    main()
