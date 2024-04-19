import yaml

class Slack:
    def __init__(self, message=None, tag_id=None, message_emoji=None, project_emoji=None, project_name=None):
        self.message = message
        self.tag_id = tag_id
        self.message_emoji = message_emoji
        self.project_emoji = project_emoji
        self.project_name = project_name

class YAMLParser:

    def __init__(self):
        pass

    def parse(self, file_path):
        try:
            with open(file_path, 'r') as file:
                yaml_data = yaml.safe_load(file)

                # Check if google_sheet_url is present
                if 'google_sheet_url' not in yaml_data:
                    raise ValueError("google_sheet_url is mandatory")

                google_sheet_url = yaml_data['google_sheet_url']

                # Parse Slack data if present
                if 'slack' in yaml_data:
                    slack_data = yaml_data['slack']
                    slack_obj = Slack(message=slack_data.get('message'),
                                    tag_id=slack_data.get('tag_id'),
                                    message_emoji=slack_data.get('message_emoji'),
                                    project_emoji=slack_data.get('project_emoji'),
                                    project_name=slack_data.get('project_name'))
                else:
                    slack_obj = None

                return google_sheet_url, slack_obj

        except FileNotFoundError:
            raise FileNotFoundError("File not found.")

        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")
        
        except AttributeError as e:
            return google_sheet_url, Slack()

        except Exception as e:
            raise ValueError(f"Error: {e}")