
import os
from enum import Enum
from LocalizationFilesReader import LocalizationFilesReader
from ArgumentParser import ArgumentParser


def search(project_directory, escaping_paths):
    folder = os.path.dirname(project_directory)
    LocalizationFilesReader().search(folder, escaping_paths)

def validate_project_path(path):
    if not path.endswith(".xcodeproj"):
        raise argparse.ArgumentTypeError("Project file must have the extension '.xcodeproj'")
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError("Project file does not exist")
    return path

def validate_config_path(path):
    if not path.endswith(".json"):
        raise argparse.ArgumentTypeError("Config file must have the extension '.json'")
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError("Config file does not exist")
    return path

def submodules(project_directory, should_include_pods=True, should_include_carthage=True):
    result = []
    folder = os.path.dirname(project_directory)
    
    if should_include_pods:
        pods_path = os.path.join(folder, "Pods")
        if os.path.exists(pods_path):
            result.append(pods_path)
    
    if should_include_carthage:
        carthage_path = os.path.join(folder, "Carthage")
        if os.path.exists(carthage_path):
            result.append(carthage_path)
    
    gitmodules_file = os.path.join(folder, ".gitmodules")
    if not os.path.exists(gitmodules_file):
        return result
    
    with open(gitmodules_file, 'r') as file:
        strings = file.read().replace("\t", "").split("\n")
        gitmodules = [os.path.join(folder, submodule.split("=")[-1].strip()) for submodule in strings if submodule.startswith("path")]
        result.extend(gitmodules)
    
    return result

def import_data(project_path, json_path):
    submodules_list = submodules(project_path)
 
    search(project_path, submodules_list)
    # Implement import functionality here

def export_data(project_path, json_path):
    print("Using project path:", project_path)
    print("Exporting data to:", project_path)
    print("Using config file:", json_path)
    submodules_list = submodules(project_path)
    print("Submodules found:")
    for submodule in submodules_list:
        print(submodule)
    # Implement export functionality here

def main():
    (command, project, config) = ArgumentParser().start()

    if command == "import":
        import_data(project, config)
    elif command == "export":
        export_data(args.config)

if __name__ == "__main__":
    main()
