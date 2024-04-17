from enum import Enum

class FileExtension(Enum):
    localizationFolder = "lproj"
    strings = "strings"
    stringsDictionary = "stringsdict"
    project = "xcodeproj"
    workspace = "xcworkspace"
    framework = "framework"