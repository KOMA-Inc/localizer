import argparse
import os

class ArgumentParser:
    def __init__(self):
        pass  # No need to initialize anything here in this context

    @staticmethod
    def validate_project_path(path):
        if not path.endswith(".xcodeproj"):
            raise argparse.ArgumentTypeError("Project file must have the extension '.xcodeproj'")
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("Project file does not exist")
        return path

    @staticmethod
    def validate_config_path(path):
        if not path.endswith(".json"):
            raise argparse.ArgumentTypeError("Config file must have the extension '.json'")
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("Config file does not exist")
        return path

    def start(self):
        parser = argparse.ArgumentParser(description="Localizer script")
        subparsers = parser.add_subparsers(title="Commands", dest="command", required=True, help="Available commands")

        for command in ["import", "export"]:
            subparser = subparsers.add_parser(command, help=f"{command.capitalize()} data")
            subparser.add_argument("-p", "--project", required=True, type=self.validate_project_path, help="Path to .xcodeproj file")
            subparser.add_argument("-c", "--config", required=True, type=self.validate_config_path, help="Path to .json config file")

        args = parser.parse_args()

        return (args.command, args.project, args.config)

        # if args.command == "import":
            # import_data(args.project, args.config)
        # elif args.command == "export":
            # export_data(args.project, args.config)


