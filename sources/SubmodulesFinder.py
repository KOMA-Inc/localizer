import os

class SubmodulesFinder:

    def __init__(self):
        pass

    def submodules(self, project_directory, should_include_pods=True, should_include_carthage=True):
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