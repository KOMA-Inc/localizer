import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp
from SlackMessanger import SlackMessanger, SlackRangeInput
from ImportInput import ImportInput

class SheetsManager:

    def __init__(self):
        pass

    def client(self, creds_file):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        return client

    def export(self, inputs, creds, sheets_url, slack_object):
        client = self.client(creds)
        sh = client.open_by_url(sheets_url)
        
        slack_inputs = []

        for input in inputs:

            try:
                sheet = sh.worksheet(input.title)
            except:
                sheet = sh.add_worksheet(input.title, rows=1000, cols=26)
            sheet.clear()
            sheet.update([input.dataframe.columns.values.tolist()] + input.dataframe.values.tolist())
            slack_inputs.append(SlackRangeInput(input.title, sheet.url, self.__analize_non_localized_ranges(input)))

        SlackMessanger().send_slack_message(slack_inputs, slack_object)
    
    def importt(self, sheets_names, creds, sheets_url):
        client = self.client(creds)
        sh = client.open_by_url(sheets_url)

        inputs = []

        for sheet_name in sheets_names:
            try:
                sheet = sh.worksheet(sheet_name)
                records = sheet.get_all_records()
                inputs.append(ImportInput(sheet_name, records))
            except:
                inputs.append(ImportInput(sheet_name, []))
        
        return inputs
        
    def __analize_non_localized_ranges(self, input):
            df = input.dataframe

            # Check if there is at least one non-empty element in a row
            non_empty_rows = (df != '').any(axis=1)

            # Check if there is at least one empty element in a row
            empty_rows = (df == '').any(axis=1)

            # Combine the conditions to find rows meeting both criteria
            mixed_rows_series = non_empty_rows & empty_rows
            mixed_rows = mixed_rows_series.index[mixed_rows_series].to_numpy()
            mixed_rows = [index + 2 for index in mixed_rows]

            return self.__group_consecutive_indexes(mixed_rows)


    def __group_consecutive_indexes(self, index_array):
        if len(index_array) == 0:
            return []

        groups = []
        current_group = [index_array[0]]

        for i in range(1, len(index_array)):
            if index_array[i] == index_array[i - 1] + 1:
                current_group.append(index_array[i])
            else:
                groups.append(current_group)
                current_group = [index_array[i]]

        # Add the last group
        groups.append(current_group)

        # Format groups as strings
        grouped_strings = []
        for group in groups:
            if len(group) == 1:
                grouped_strings.append(str(group[0]))
            else:
                grouped_strings.append(f"{group[0]}-{group[-1]}")

        return grouped_strings