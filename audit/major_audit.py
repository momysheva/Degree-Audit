import pandas as pd
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe
from id import get_unique_ids
import check
import electives
import extract
import kaz
from time import sleep
from googleapiclient.discovery import build
from coloring import color

GOOGLE_DRIVE_CREDENTIALS_FILE = '/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_DRIVE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

drive_service = build('drive', 'v3', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)

grades={'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.7, 'D+':1.3, 'D':1.0, 'F':0.0,'SD':3.0}
seds=['CEE','ENG','ELCE','CHME','MAE','CSCI','ROBT']
smg=['MINE','SMG','GEOL','PETE']
soc_elective=['ANT','ECON','PLS','SOC']
hum_electives=['HST', 'PHIL','REL','WLL']

def create_folder(folder_name, parent_folder_id='1OpfooxTPkdZEWjt6NSNGjZzQ_5A4NlA5'):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]  # Specify the parent folder ID
    }
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def find_spreadsheet_in_folder(title,folder_id='1OpfooxTPkdZEWjt6NSNGjZzQ_5A4NlA5'):
    query = f"'{folder_id}' in parents and name='{title}' and mimeType='application/vnd.google-apps.spreadsheet'"
    response = drive_service.files().list(q=query).execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']  # Returns the ID of the first matching file
    return None

def get_number_for_keyword(data, keyword):
        # Split the string into segments based on '|'
        segments = data.split('|')
        # Iterate through each segment
        for segment in segments:
            # Split each segment into parts (assuming the keyword and number are separated by a space)
            parts = segment.split()

            if parts[0].lower() == keyword.lower():
                # Return the number associated with the keyword
                return parts[1]
        return None 

def major_check(major):
    unique_ids = get_unique_ids(major)
    print(len(unique_ids))
    final_major=pd.DataFrame(columns=['ID','Requirements'])
    # spreadsheet_title = 'Audit'
    # spreadsheet = client.open(spreadsheet_title)
    # sheet_name = major
    # sheet = spreadsheet.worksheet(sheet_name)
    # values = sheet.get_all_values()

    spreadsheet_title = 'Audit'
    spreadsheet_id = find_spreadsheet_in_folder(spreadsheet_title)
    if spreadsheet_id:
        spreadsheet = client.open_by_key(spreadsheet_id)
        sheet_name = major
        sheet = spreadsheet.worksheet(sheet_name)
        values = sheet.get_all_values()
    else:
        print("Spreadsheet not found in the specified folder.")


    humanities=electives.humanities()
    hum_soc=electives.hum_soc()
    general=electives.general()
    folder_id = create_folder(f'{major}')


    for id in unique_ids:
        credits=0
        differences=0
        second_check=[]
        courses_passed=[]
        course_req_strict=[]
        course_req_open=[]

        sleep(1)
        
        kaz_courses=extract.extract(id,major,folder_id)
        # if major=='SOC' or major=='ANT' or major=='PLS' or major=='ECON' or major=='HST' or major=='WLL':
        level=kaz.check_kaz_level(kaz_courses)
        # else:
        #     level=kaz.check_kaz_level_non_ba(kaz_courses)

        for row in values[1:]:
            if row[0].endswith('xx') or 'xx' in row[0] or '/' in row[0] or row[0]=='Social Sciences Elective' or row[0]=='Humanities elective' or row[0]=='General Elective' :
                if row[0].strip()=='KAZ xxx':
                    kaz_c=get_number_for_keyword(row[5],level)
                    if kaz_c:
                        if level=='foreign':
                            course_req_open.append((f'KFL {kaz_c}',row[1],'8',row[3].replace(" and above", ""),row[4],row[5]))
                        else:
                            course_req_open.append((f'KAZ {kaz_c}',row[1],row[2],row[3].replace(" and above", ""),row[4],row[5]))

                else:
    
                    course_req_open.append((row[0].strip(),row[1],row[2],row[3].replace(" and above", ""),row[4],row[5]))
            else:
                course_req_strict.append((row[0].strip(),row[1],row[2],row[3].replace(" and above", ""),row[4],row[5]))


        spreadsheet_title_student = major+str(id)
        sleep(2)
        spreadsheet = client.open(spreadsheet_title_student)
        sheet_name = 'Sheet1'
        sheet_student = spreadsheet.worksheet(sheet_name)
        values_student = sheet_student.get_all_values()

        student_courses=[]
        for row in values_student[1:]:
            if len(row[1])==2:
                student_courses.append((row[0],'0'+row[1],row[2],row[4],row[3],row[5]))
            else:
                student_courses.append((row[0],row[1],row[2],row[4],row[3],row[5])) #abbr code title credit grade term

                
        for course in student_courses:
            result=check.search(course_req_open, course_req_strict,course, major,hum_soc,soc_elective,grades,seds,smg, hum_electives,humanities,general)
            if result==None:
                courses_passed.append('N\A')
                credits+=int(course[3])
                differences+=int(course[3])
                second_check.append(course)
            else:
                status,name,req_course=result
                if len(course_req_strict)!=0:
                    if req_course in course_req_strict:
                        if status:
                            if int(course[3])>int(req_course[2].split('/')[0]):
                                differences+=int(course[3])-int(req_course[2].split('/')[0])
                            courses_passed.append(req_course[0])
                            credits+=int(course[3])
                            course_req_strict.remove(req_course)
                        else:
                            courses_passed.append('Fail')
                    elif len(course_req_open)!=0:
                        if req_course in course_req_open:
                            if status:
                                if int(course[3])>int(req_course[2].split('/')[0]):
                                    differences+=int(course[3])-int(req_course[2].split('/')[0])
                                courses_passed.append(req_course[0])
                                if req_course[5].split('|')[0]==course[3]:
                                    found=next((item for item in course_req_open if item[0] == req_course[5].split('|')[1]), None)
                                    if found:
                                        course_req_open.remove(found)
                                credits+=int(course[3])
                                course_req_open.remove(req_course)
                            else:
                                courses_passed.append('Fail')
                    
                elif len(course_req_open)!=0:
                    if req_course in course_req_open:
                        if status:
                            if int(course[3])>int(req_course[2].split('/')[0]):
                                differences+=int(course[3])-int(req_course[2].split('/')[0])
                            courses_passed.append(req_course[0])
                            if req_course[5].split('|')[0]==course[3]:
                                found=next((item for item in course_req_open if item[0] == req_course[5].split('|')[1]), None)
                                if found:
                                
                                    course_req_open.remove(found)
                            credits+=int(course[3])
                            course_req_open.remove(req_course)
                        else:
                            courses_passed.append('Fail')

        general_credits=0
        if major=='BIOL':
            found=next((item for item in course_req_open if item[0] == 'BIOL 3xx/4xx'), None)
            if found:
                if second_check:
                    credit=0
                    for course in second_check:
                        if course[0]=='BIOL' and (course[1][0]=='3' or course[1][0]=='4'):
                            credit+=int(course[3])
                    if credit>=6:
                        differences-=credit
                        course_req_open.remove(found)                

        if credits>=240:
            found=next((item for item in course_req_open if item[0] == 'Open xxx' or item[0]=="General Elective"), None)
            if found:
                course_req_open = [item for item in course_req_open if item[0] != "General Elective" and item[0] != "Open xxx"]

        else:
            if course_req_open:
                # general_elective_count = sum(1 for item in course_req_open if (item[0] == "General Elective" or item[0] == "Open xxx"))
                general_credits = sum(int(item[2].split('/')[0]) for item in course_req_open if item[0] == "General Elective" or item[0] == "Open xxx")

                print(general_credits)
                if general_credits!=0:
                    # general_credits=general_elective_count*6
                    print(general_credits)
                    print(differences)
                    if differences<=general_credits:
                        general_credits=general_credits-differences
                    else:
                        general_credits=0
                    course_req_open = [item for item in course_req_open if item[0] != "General Elective" and item[0] != "Open xxx"]


            # spreadsheet_title_student = 'BIOL'+str(id)
        # spreadsheet = client.open(spreadsheet_title_student)
        # sheet_name = 'Sheet1'
        if course_req_open or course_req_strict:
            # if course_req_open:
            #     for c in second_check:

            # combined_data = ((','.join(','.join(t) for t in course_req_strict) + ';' if course_req_strict else '') +
            #         ','.join(','.join(t) for t in course_req_open))
            combined_data = ((','.join(t[0] for t in course_req_strict) + ';' if course_req_strict else '') +
                    ','.join(t[0] for t in course_req_open))
            if general_credits!=0:  # Check if general_credits is defined
                combined_data += f';General Credits:{general_credits}'
            
        else:
            if general_credits!=0:  # Check if general_credits is defined
                combined_data = f'General Credits:{general_credits}'
            else:
                combined_data = 'All requirements'
            
        

        # sheet_student = spreadsheet.worksheet(sheet_name)
        existing_data = sheet_student.get_all_records()
        courses_passed = ['Technical Elective' if 'SEDS' in course else course for course in courses_passed]


        df = pd.DataFrame(existing_data)
        df['Test'] = courses_passed
        new_row = [None] * len(df.columns)  # Assuming all columns are filled with None initially
        new_row[-1] = combined_data  # Assuming 'Test' column is the last column
        df.loc[len(df)] = new_row
        new_data = df.astype(str).values.tolist()


        sheet_student.clear()
        set_with_dataframe(sheet_student, df)
        color(spreadsheet_title_student)

        # new_row = {'ID': id, 'Requirements': combined_data}
        # final_major = final_major.append(new_row, ignore_index=True)
        data_to_add = {'ID': [id], 'Requirements': [combined_data]}
        new_data = pd.DataFrame(data_to_add)
        final_major = pd.concat([final_major, new_data], ignore_index=True)
        print('Tested ',id)

    spreadsheet_title = major+' Final'
    spreadsheet = client.create(spreadsheet_title)

    # folder_id = '1kPjjtGIHftqmDCMqe9WfU9R805-jir5M'
    spreadsheet = client.create(spreadsheet_title, folder_id='1OpfooxTPkdZEWjt6NSNGjZzQ_5A4NlA5')
    worksheet = spreadsheet.get_worksheet(0)
    set_with_dataframe(worksheet, final_major)
    print('Done!')
                        

