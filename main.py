import os
from LocalizationFilesReader import LocalizationFilesReader
from ArgumentParser import ArgumentParser
from sources.Exporter import Exporter

def import_data(project_path, json_path):
   print("To do")

def export_data(project_path, json_path):
    Exporter().export_strings(project_path)

def main():
    (command, project, config) = ArgumentParser().start()

    if command == "import":
        import_data(project, config)
    elif command == "export":
        export_data(project, config)

if __name__ == "__main__":
    main()
