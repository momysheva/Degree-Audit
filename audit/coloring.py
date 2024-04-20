import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Authenticate and create the client
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json', scope)
client = gspread.authorize(creds)

def color(name):
    sheet = client.open(name).sheet1

    # Google Sheets API setup
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = sheet.spreadsheet.id

    # Conditional formatting request to color entire rows based on "grade" column
    request = {
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": sheet._properties['sheetId'],
                    "startRowIndex": 1,  # Assuming header is in the first row, start at second row
                    "endRowIndex": sheet.row_count,  # Apply to all data rows
                }],
                "booleanRule": {
                    "condition": {
                        "type": "TEXT_EQ",
                        "values": [{
                            "userEnteredValue": "in progress"  # Text to match in the grade column
                        }]
                    },
                    "format": {
                        "backgroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 0.0  # Yellow color
                        }
                    }
                }
            },
            "index": 0
        }
    }

    # Send the request to the API to apply the rule
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": [request]}).execute()
