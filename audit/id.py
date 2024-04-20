import pandas as pd
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe

GOOGLE_DRIVE_CREDENTIALS_FILE = '/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_DRIVE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)



def get_unique_ids(sheet_name):
    sheet = client.open('Degree Audit')
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    id_set = set(df['STUDENTID'])

    return id_set

