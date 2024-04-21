import requests
import json

class SlackRangeInput:

    def __init__(self, name, url, ranges) -> None:
        self.name = name
        self.url = url
        self.ranges = ranges

class SlackMessanger:

    def __init__(self):
        pass

    def send_slack_message(self, slack_inputs, slack_object):
        if slack_object is None:
            return
        
        contains_non_empty = any(input.ranges for input in slack_inputs if input.ranges)

        if contains_non_empty == False:
            return
        
        if slack_object.message is None:
            message = ""
        else:
            message = slack_object.message
        
        if slack_object.tag_id is not None:
            if len(message) == 0:
                message = f"<@{slack_object.tag_id}>!"
            else:
                message += f", <@{slack_object.tag_id}>!"
        
        if slack_object.message_emoji is None:
            if len(message) > 0:
                message += "\n"
        else:
            if len(message) == 0:
                message = f"{slack_object.message_emoji}\n"
            else:
                message += f" {slack_object.message_emoji}\n"
        
        if slack_object.project_emoji is not None or slack_object.project_name is not None:
            second_line_start = "I've added some strings for"
        else:
            second_line_start = "I've added some strings"

        message += " ".join(filter(None, [second_line_start, slack_object.project_emoji, slack_object.project_name]))
        message += "\nCurrent list of unlocalized strings:\n"

        for input in slack_inputs:
            if input.ranges:
                message += f"\n<{input.url}|{input.name}>\n" 
                for range in input.ranges:
                    message += f"•  {range}\n"

        payload = {
            "text": message
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            slack_object.webhook_url,
            data=json.dumps(payload),
            headers=headers
        )