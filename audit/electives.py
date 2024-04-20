
import pandas as pd
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread

GOOGLE_DRIVE_CREDENTIALS_FILE = '/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_DRIVE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

electives = 'Electives'

def humanities(electives = 'Electives'):
    electives_spreadsheet = client.open(electives)
    sheet_name = 'hum'
    sheet = electives_spreadsheet.worksheet(sheet_name)
    values = sheet.get_all_values()
    column_headers = values[0]
    num_columns = len(column_headers)
    humanities = [[] for _ in range(num_columns)]
    for row in values: 
        for col_idx, value in enumerate(row):
            if value!='':
                humanities[col_idx].append(value)
    return humanities



def hum_soc(electives = 'Electives'):
    electives_spreadsheet = client.open(electives)
    sheet_name = 'Hum/Soc'
    sheet = electives_spreadsheet.worksheet(sheet_name)
    values = sheet.get_all_values()
    column_headers = values[0]
    num_columns = len(column_headers)
    hum_soc = [[] for _ in range(num_columns)]
    for row in values: 
        for col_idx, value in enumerate(row):
            if value!='':
                hum_soc[col_idx].append(value)
    return hum_soc


def general(electives = 'Electives'):
    electives_spreadsheet = client.open(electives)
    sheet_name = 'General'
    sheet = electives_spreadsheet.worksheet(sheet_name)
    values = sheet.get_all_values()
    column_headers = values[0]
    num_columns = len(column_headers)
    general = [[] for _ in range(num_columns)]
    for row in values: 
        for col_idx, value in enumerate(row):
            if value!='':
                general[col_idx].append(value)
    return general


# spreadsheet_title = 'Audit sort'
# spreadsheet = client.open(spreadsheet_title)
# sheet_name = 'Лист1'
# sheet = spreadsheet.worksheet(sheet_name)
# all_records = sheet.get_all_values()

# df = pd.DataFrame(all_records[1:], columns=all_records[0])


# # Sort the DataFrame by the first two columns
# sorted_df = df.sort_values(by=[df.columns[0], df.columns[1]])
# print(sorted_df)

# # Clear the worksheet
# sheet.clear()

# # Append the sorted records to the worksheet
# sheet.append_row(all_records[0])  # Append header row
# for _, row in sorted_df.iterrows():
#     sheet.append_row(row.tolist())

# print("Spreadsheet sorted successfully!")