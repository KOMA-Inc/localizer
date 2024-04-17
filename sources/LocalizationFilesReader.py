import os
from LProjName import LProjName
from LocalizationFile import LocalizationFile

class LocalizationFilesReader:
    def __init__(self):
        pass
    
    def search(self, url, escaping_paths):
        folder = os.path.dirname(url)
        locations = self.__fetch_localization_folders(folder, escaping_paths)

        result = []
        for location in locations:
            files = os.listdir(location)
            for file in files:
                language_folder = LProjName.create(location)
                if language_folder:
                    item = LocalizationFile.create(location + "/" + file, language_folder)
                    if item:
                        result.append(item)
        return result
    
    def __fetch_localization_folders(self, url, urls):
        folders = []
        for root, dir, files in os.walk(url):
            if not self.__should_skip_root(root, urls) and os.path.splitext(root)[1] == ".lproj":
                folders.append(root)
        
        return folders

    def __should_skip_root(self, root, urls):
        for skip_url in urls:
            if root.startswith(skip_url):
                return True
        return False