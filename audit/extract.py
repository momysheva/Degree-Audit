import pandas as pd
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe
from googleapiclient.discovery import build

GOOGLE_DRIVE_CREDENTIALS_FILE = '/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_DRIVE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

drive_service = build('drive', 'v3', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)

def find_spreadsheet_in_folder(title,folder_id='1OpfooxTPkdZEWjt6NSNGjZzQ_5A4NlA5'):
    query = f"'{folder_id}' in parents and name='{title}' and mimeType='application/vnd.google-apps.spreadsheet'"
    response = drive_service.files().list(q=query).execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']  # Returns the ID of the first matching file
    return None

def extract(student_id,major, folder_id):
    print('Extracting data for student ID:',student_id)
    # spreadsheet_title = 'Degree Audit'
    # spreadsheet = client.open(spreadsheet_title)
    # sheet_name = major
    # sheet = spreadsheet.worksheet(sheet_name)
    # values = sheet.get_all_values()

    spreadsheet_title = 'Degree Audit'
    spreadsheet_id = find_spreadsheet_in_folder(spreadsheet_title)
    if spreadsheet_id:
        spreadsheet = client.open_by_key(spreadsheet_id)
        sheet_name = major
        sheet = spreadsheet.worksheet(sheet_name)
        values = sheet.get_all_values()
    else:
        print("Spreadsheet not found in the specified folder.")
    student_courses=[]
    special_case=[]
    kaz=[]
    for row in values[1:]:
        if row[0]==student_id:
            if row[6]!="NUM" and "RT" not in row[6] and 'UD' not in row[6] and "F" not in row[6] and row[6]!='AU':
                if row[3]=='KAZ' or row[3]=='KFL':
                    kaz.append((row[3],row[4]))

                if row[3]=='SHSS' and (row[4]=='150' or row[4][0]=='2'):
                    if ('WCS',row[4],row[5],row[6],row[7],row[8]) not in student_courses:
                        student_courses.append(('WCS',row[4],row[5],row[6],row[7],row[8]))    

                elif row[3]=='CHEM' and row[4]=='212' and major=='BIOL':
                    special_case.append((row[3],row[4]))
                    if len(special_case)==2:
                        student_courses.append(('CHEM','212',special_case[0][2],special_case[0][3],'8',special_case[0][5]))
                    else:
                        continue

                elif major=="SOC":
                    found=next((item for item in student_courses if item[2] == row[5]), None)
                    if found:
                        student_courses.remove(found)
                        student_courses.append((row[3],row[4],row[5],row[6],row[7],row[8]))
                elif major=="ANT" or major=='WLL' or (major=='PLS' and row[4]!='395'):
                    found = next((item for item in student_courses if tuple(x.strip() for x in item[2:]) == tuple(x.strip() for x in row[5:])), None)
                    # found=next((item for item in student_courses if item[2:] == row[5:]), None)
                    if found:
                        continue
                    else:
                        found = next((item for item in student_courses if tuple(x.strip() for x in item[:3]) == tuple(x.strip() for x in row[3:6])), None)
                        if found and row[4]!="395":
                            student_courses.remove(found)
                            student_courses.append((row[3],row[4],row[5],row[6],row[7],row[8]))
                            
                        elif (row[3],row[4],row[5],row[6],row[7],row[8]) not in student_courses:
                            student_courses.append((row[3],row[4].replace('L',''),row[5],row[6],row[7],row[8]))
    

                else:
                    found = next((item for item in student_courses if tuple(x.strip() for x in item[:3]) == tuple(x.strip() for x in row[3:6])), None)
                    if found:
                        student_courses.remove(found)
                        student_courses.append((row[3],row[4],row[5],row[6],row[7],row[8]))
                               
                    elif (row[3],row[4],row[5],row[6],row[7],row[8]) not in student_courses:
                        student_courses.append((row[3],row[4].replace('L',''),row[5],row[6],row[7],row[8]))
    if len(special_case)==1:
        student_courses.append((special_case[0][0],special_case[0][1],special_case[0][2],special_case[0][3],special_case[0][4],special_case[0][5]))

    df = pd.DataFrame(student_courses, columns=['ABBR', 'CODE', 'Title', 'Grade', 'Credit', 'Term'])


    # custom_order = ['ANT', 'PLS', 'SOC']
    # high_precedence_codes = ['200', '230', '240']
    # low_precedence_codes = ['204', '205', '206', '210', '220', '250']
    # all_special_wcs_codes = high_precedence_codes + low_precedence_codes

    # # Filter and maintain the order for 'ANT', 'PLS', 'SOC'
    # mask_custom_order = df['ABBR'].isin(custom_order)
    # df_custom_order = df[mask_custom_order]

    # # Filter and sort 'WCS' entries based on special codes, sorting within those codes
    # mask_wcs = df['ABBR'].eq('WCS') & df['CODE'].isin(all_special_wcs_codes)
    # df_wcs = df[mask_wcs].sort_values(by='CODE')

    # # Filter and maintain the order for 'ECON'
    # df_econ = df[df['ABBR'] == 'ECON']

    # # All other entries
    # mask_others = ~(df['ABBR'].isin(custom_order) | df['ABBR'].eq('WCS') & df['CODE'].isin(all_special_wcs_codes) | df['ABBR'].eq('ECON'))
    # df_others = df[mask_others]

    # # Concatenate in the desired order
    # sorted_df = pd.concat([df_custom_order, df_others, df_wcs, df_econ])

    df['TermYear'] = df['Term'].str.extract('(\d+)').astype(int)  # Extract year and convert to integer

    # custom_order = ['ANT', 'PLS', 'SOC']
    custom_order = {'ANT': 1, 'PLS': 2, 'SOC': 3}
    high_precedence_codes = ['200', '230', '240']
    low_precedence_codes = ['204', '205', '206', '210', '220', '250']
    all_special_wcs_codes = high_precedence_codes + low_precedence_codes
    

    # Apply sorting to each segment based on 'TermYear'
    # df_custom_order = df[df['ABBR'].isin(custom_order)].sort_values(by='TermYear')
    # df_custom_order = df[df['ABBR'].isin(custom_order)].copy()
    # df_custom_order.loc[:, 'SortKey'] = df_custom_order['ABBR'].map(custom_order)
    # df_custom_order = df_custom_order.sort_values(by=['SortKey', 'TermYear'])
    # df_custom_order.drop(columns='SortKey', inplace=True)  

    df_custom_order = df[df['ABBR'].isin(custom_order.keys())].copy()
    df_custom_order.loc[:, 'SortKey'] = df_custom_order['ABBR'].map(custom_order)
    df_custom_order.loc[:, 'SpecialSortKey'] = df_custom_order.apply(lambda row: 0 if (row['ABBR'] == 'PLS' and row['CODE'] == '395') else 1, axis=1)
    df_custom_order = df_custom_order.sort_values(by=['SortKey', 'SpecialSortKey', 'TermYear'])
    df_custom_order.drop(columns=['SortKey', 'SpecialSortKey'], inplace=True)

    df_wcs = df[df['ABBR'].eq('WCS') & df['CODE'].isin(all_special_wcs_codes)].sort_values(by=['CODE', 'TermYear'])
    df_econ = df[df['ABBR'] == 'ECON'].sort_values(by='TermYear')
    df_others = df[~(df['ABBR'].isin(custom_order) | (df['ABBR'].eq('WCS') & df['CODE'].isin(all_special_wcs_codes)) | df['ABBR'].eq('ECON'))]

    # Concatenate in the desired order with the added term sort
    sorted_df = pd.concat([df_custom_order, df_others, df_wcs, df_econ])




    spreadsheet_title = major+str(student_id)
    spreadsheet = client.create(spreadsheet_title)

    # folder_id = '1kPjjtGIHftqmDCMqe9WfU9R805-jir5M'
    spreadsheet = client.create(spreadsheet_title, folder_id=folder_id)
    worksheet = spreadsheet.get_worksheet(0)
    set_with_dataframe(worksheet, sorted_df)
    return kaz
