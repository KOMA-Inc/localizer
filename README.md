# localizer

Features:

- Export .strings files from Xcode project to Google Sheets
- Import .strings files from Google Sheets to Xcode project
- Sending messages to Slack

## Usage

### Create a service accout

1. [Go to Google API Console](https://console.cloud.google.com/apis/dashboard)
2. Create new project
3. Go to API's overview
4. Add Google Drive API
5. Add Google Sheets API
6. Go to Manage in Google Drive API
7. Open Credentials -> Create Credentials -> Service account
8. Enter name for your project
9. For role select Basic -> Editor
10. Click on the Service account you just created
11. Go to Keys -> Create new key -> JSON
12. Save your creds.json file

### Create .yaml config file

Download the [example](https://github.com/KOMA-Inc/localizer/blob/main/config_example.yml) and update it for your needs.  
To get the tag_id to your colleague's account is Slack and tap "Copy memeber ID"

### Run the script

Import:
```bash
python3 localizer/sources/main.py import -p ./MyProject.xcodeproj -c ./creds.json -y ./lconfig.yml
```

Export:
```bash
python3 localizer/sources/main.py export -p ./MyProject.xcodeproj -c ./creds.json -y ./lconfig.yml
```
