import pandas as pd
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe
import id

GOOGLE_DRIVE_CREDENTIALS_FILE = '/home/aliza/Documents/projects/ssh_telegram_bot/bot/sshbot-401810-507d88f6b018.json'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_DRIVE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

grades={'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.7, 'D+':1.3, 'D':1.0, 'F':0.0,'SD':2.0}
courses_passed=[]
seds=['CEE','ENG','ELCE','CHME','MAE','CSCI','ROBT']
smg=['MINE','SMG','GEOL','PETE']
soc_elective=['ANT','ECON','PLS','SOC']
hum_electives=['HST', 'PHIL','REL','WLL']

unique_ids = id.get_unique_ids('BIOL')

spreadsheet_title = 'Audit'
spreadsheet = client.open(spreadsheet_title)
sheet_name = 'BIOL'
sheet = spreadsheet.worksheet(sheet_name)
values = sheet.get_all_values()
course_req_strict=[]
course_req_open=[]
for row in values[1:]:
    if row[0].endswith('xx') or 'xx' in row[0] or '/' in row[0] or row[0]=='Social Sciences Elective' or row[0]=='Humanities elective' or row[0]=='General Elective' :
        course_req_open.append((row[0].strip(),row[1],row[2],row[3].replace(" and above", ""),row[4]))
    else:
        course_req_strict.append((row[0].strip(),row[1],row[2],row[3].replace(" and above", ""),row[4]))


electives = 'Electives'
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

spreadsheet_title_student = 'BIOL Audit'
spreadsheet = client.open(spreadsheet_title_student)
sheet_name = '201876125'
sheet_student = spreadsheet.worksheet(sheet_name)
values_student = sheet_student.get_all_values()

student_courses=[]
for row in values_student[1:]:
    if len(row[1])==2:
        student_courses.append((row[0],'0'+row[1],row[2],row[4],row[3],row[5]))
    else:
        student_courses.append((row[0],row[1],row[2],row[4],row[3],row[5]))




def find_in_strict(coure_req_strict, target):
    for course in coure_req_strict:
        req=course[0].split('|')
        if any(target[0] in s for s in req):
            if any(target[1] in s for s in req):
                if course[1]!='':
                    if target[2] in course[1]:
                        if target[3] in course[2]:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                courses_passed.append(course)
                                return (True, 'strict',course)
                            else:
                                courses_passed.append('Fail')
                                return (False, 'strict', course)
                else:
                    if target[3] in course[2]:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            courses_passed.append(course)
                            return (True, 'strict',course)
                        else:
                            courses_passed.append('Fail')
                            return (False, 'strict', course)
                    else:
                        courses_passed.append('Fail')
                        return (False, 'strict', course)
    return None

def find_in_open(course_req_open, target, major,hum_soc,soc_elective):
    for course in course_req_open:
        print('target',target)
        req=course[0].split('|')
        print('req',req)
        found=next((s for s in req if target[0] in s), None)
        if found:
            codes=found.split(' ')[1].split('/')
            print('codes',codes)
            for code in codes:
                if code=='xxx':
                    if target[0]+' '+target[1] not in course[4]:
                        if target[3] in course[2]:
                            if  (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                courses_passed.append(course)
                                return (True, 'open',course)
                            else:
                                courses_passed.append('Fail')
                                return (False, 'strict', course)
                       
                elif code.endswith('xx'):
                    if target[0]+' '+target[1] not in course[4]:
                        if code[0]==target[1][0]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    continue
                                    #return (False, 'open',course)
                        else:
                            continue
                elif code==target[1]:
                    if target[3] in course[2]:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            courses_passed.append(course)
                            return (True, 'open',course)
                        else:
                            courses_passed.append('Fail')
                            return (False, 'strict', course)


        elif next((s for s in req if 'SEDS' in s), None):
            found=next((s for s in req if 'SEDS' in s), None)
            if target[0] in seds:
                codes=found.split(' ')[1].split('/')
                for code in codes:
                    if code=='xxx':
                        if target[0]+' '+target[1] not in course[4]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    courses_passed.append('Fail')
                                    return (False, 'strict', course)
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        courses_passed.append(course)
                                        return (True, 'open',course)
                                    else:
                                        continue
                        
            elif target[0] in smg:
                found=next((s for s in req if 'SMG' in s), None)
                codes=found.split(' ')[1].split('/')
                for code in codes:
                    if code=='xxx':
                        if target[0]+' '+target[1] not in course[4]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    courses_passed.append('Fail')
                                    return (False, 'strict', course)
                        
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        courses_passed.append(course)
                                        return (True, 'open',course)

                                    else:
                                        continue      
        elif next((s for s in req if 'SMG' in s), None):
            found=next((s for s in req if 'SMG' in s), None)
            if target[0] in smg:
                codes=found.split(' ')[1].split('/')
                for code in codes:
                    if code=='xxx':
                        if target[0]+' '+target[1] not in course[4]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    courses_passed.append('Fail')
                                    return (False, 'strict', course)
                        
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        courses_passed.append(course)
                                        return (True, 'open',course)

                                    else:
                                        continue

            
        elif course[0]=='Social Sciences Elective':
            hum_soc_electives, soc_elective_courses=check_soc_elective(hum_soc,soc_elective,major)
            if target[0] in soc_elective_courses:
                if target[0]+' '+target[1] not in course[4]:
                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                        courses_passed.append(course)
                        return (True, 'open',course)
            else:
                for term in hum_soc_electives:
                    if int(target[5])>=int(term[0]):
                        if target[0]+' '+target[1] in term:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                courses_passed.append(course)
                                return (True, 'open',course)
                            else:
                                courses_passed.append('Fail')
                                return (False, 'strict', course)
                        elif any('xxx' in s for s in term):
                            for s in term:
                                if "xxx" in s:
                                    if target[0] in s:
                                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                            courses_passed.append(course)
                                            return (True, 'open',course)
                                        else:
                                            courses_passed.append('Fail')
                                            return (False, 'strict', course)
                    else:
                        if ('General elective', '', '6', 'D', '') in course_req_open:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                courses_passed.append(('General elective', '', '6', 'D', ''))
                                return (True, 'open',('General elective', '', '6', 'D', ''))
                            else:
                                courses_passed.append('Fail')
                                return (False, 'open',('General elective', '', '6', 'D', ''))
                        

        elif course[0]=="Humanities elective":
            hum_soc_electives, hum_elective_courses, hum=check_hum_elective(hum_soc,hum_electives,major,humanities)
            if target[0] in hum_elective_courses:
                if target[0]+' '+target[1] not in course[4]:
                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                        courses_passed.append(course)
                        return (True, 'open',course)
            else:
                for term in hum:
                    if int(target[5])>=int(term[0]):
                        if target[0]+' '+target[1] in term:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                courses_passed.append(course)
                                return (True, 'open',course)
                            else:
                                courses_passed.append('Fail')
                                return (False, 'strict', course)
                    
                for term in hum_soc:
                        if int(target[5])>=int(term[0]):
                            if target[0]+' '+target[1] in term:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    courses_passed.append('Fail')
                                    return (False, 'strict', course)
                            elif any('xxx' in s for s in term):
                                for s in term:
                                    if "xxx" in s:
                                        if target[0] in s:
                                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                                courses_passed.append(course)
                                                return (True, 'open',course)
                                            else:
                                                courses_passed.append('Fail')
                                                return (False, 'strict', course)
                if target[0] in ['CHN','FRE','GER','KFL','KOR','PER','RFL','SPA'] or target[0]+' '+ target[1] in ['TUR 301','TUR 305', 'TUR 411', 'TUR 412']:
                    if int(target[5])<541:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            courses_passed.append(course)
                            return (True, 'open',course)

        elif course[0] =='Open xxx' or course[0]=='General Elective':
            if course[0]=='General Elective':
                for term in general:
                        if target[0]+' '+target[1] in term:
                            if int(target[5])>=int(term[0]):
                                if target[0]+' '+target[1] not in course[4]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        courses_passed.append(course)
                                        return (True, 'open',course)
                                    else:
                                        courses_passed.append('Fail')
                                        return (False, 'strict', course)
                            else:
                                if ('Humanities elective', '', '6', 'D', '') in course_req_open:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        courses_passed.append(('Humanities elective', '', '6', 'D', ''))
                                        return (True, 'open',('Humanities elective', '', '6', 'D', ''))
                                    else:
                                        return (False, 'open',('Humanities elective', '', '6', 'D', ''))

                        elif target[0]+' '+'xxx' in term:
                                if int(target[5])>=int(term[0]):
                                    if target[0]+' '+target[1] not in course[4]:
                                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                            courses_passed.append(course)
                                            return (True, 'open',course)
                                        else:
                                            return (False, 'open',course)
                                else:
                                    if ('Humanities elective', '', '6', 'D', '') in course_req_open:
                                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                            courses_passed.append(('Humanities elective', '', '6', 'D', ''))
                                            return (True, 'open',('Humanities elective', '', '6', 'D', ''))
                                        else:
                                            return (False, 'open',('Humanities elective', '', '6', 'D', ''))

                        else:
                            if target[0]+' '+target[1] not in course[4]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    courses_passed.append(course)
                                    return (True, 'open',course)
                                else:
                                    return (False, 'open',course)

            elif target[3] in course[2]:
                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                    courses_passed.append(course)
                    return (True, 'open',course)
                else:
                    return (False, 'open',course)



    return None

def check_soc_elective(hum_soc,soc_elective,major):
    soc_elective_courses=[course for course in soc_elective if course != major]
    for l in hum_soc:
        if any(major in s for s in l):
            new_l = [s for s in l if major not in s]
            if new_l:
                hum_soc.remove(l)
                hum_soc.append(new_l)
    
    return hum_soc, soc_elective_courses

def check_hum_elective(hum_soc,hum_electives,major, hum):
    hum_elective_courses=[course for course in hum_electives if course != major]
    for l in hum_soc:
        if any(major in s for s in l):
            new_l = [s for s in l if major not in s]
            if new_l:
                hum_soc.remove(l)
                hum_soc.append(new_l)
    for col in hum:
        if any(major in s for s in col):
            new_l = [s for s in col if major not in s]
            if new_l:
                hum.remove(col)
                hum.append(new_l)

    
    return hum_soc, hum_elective_courses, hum


def search(course_req_strict, course_req_open,target):
    result=find_in_strict(course_req_strict, target)
    print(result)
    if result:
        return result
    else:
        result=find_in_open(course_req_open,target,'BIOL',hum_soc,soc_elective)
        print(result)
        if result:
            return result
        else:
            courses_passed.append(r'N\A')
            return (True, 'N\a', 'N\a')
        
for course in student_courses:
    status,name,req_course=search(course_req_strict,course_req_open, course)
    if len(course_req_strict)!=0:
        if req_course in course_req_strict:
            if status:
                courses_passed.append(req_course)
                course_req_strict.remove(req_course)
            else:
                courses_passed.append('Fail')
        elif len(course_req_open)!=0:
            if req_course in course_req_open:
                if status:
                    courses_passed.append(req_course)
                    course_req_open.remove(req_course)
                else:
                    courses_passed.append('Fail')
        
    elif len(course_req_open)!=0:
        if req_course in course_req_open:
            if status:
                courses_passed.append(req_course)
                course_req_open.remove(req_course)
            else:
                courses_passed.append('Fail')
    

print(courses_passed)
print('\n')
print(course_req_open)
print('\n')
print(course_req_strict)
spreadsheet_title_student = 'BIOL Audit'
spreadsheet = client.open(spreadsheet_title_student)
sheet_name = '201876125'


sheet_student = spreadsheet.worksheet(sheet_name)
existing_data = sheet_student.get_all_records()
df = pd.DataFrame(existing_data)
# print(df)
df['Test'] = courses_passed
# print(df)
new_data = df.astype(str).values.tolist()
# print(new_data)

# Clear the worksheet
sheet_student.clear()
set_with_dataframe(sheet_student, df)

# Append the sorted records to the worksheet
# sheet_student.append_row(existing_data[0])  # Append header row
# sheet_student.append_row(new_data)

# Update the Google Spreadsheet with the new data
# sheet_student.update( new_data)  # Change 'A1' to the desired starting cell
# sheet_student.update(range_name='A1', values=new_data)
# print("New column added successfully.")
                      

