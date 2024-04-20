def find_in_strict(coure_req_strict, target, grades):
    for course in coure_req_strict:
        req=course[0].split('|')
        if any(target[0] in s for s in req):
            if any(target[1] in s for s in req):
                if course[1]!='':
                    # if target[2] in course[1]:
                        if target[3] in course[2]:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                return (True, 'strict',course)
                            else:
                                return (False, 'strict', course)
                else:
                    if target[3] in course[2]:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            return (True, 'strict',course)
                        else:
                            return (False, 'strict', course)
                    else:
                        return (False, 'strict', course)
    return None

def find_in_open(course_req_open, target, major,hum_soc,soc_elective,grades,seds,smg, hum_electives,humanities,general):
    for course in course_req_open:
        req=course[0].split('|')
        found=next((s for s in req if target[0] in s), None)
        if found:
            codes=found.split(' ')[1].split('/')
            for code in codes:
                if '-' in code:
                    if target[1][0]==code[0]:
        # print(code.split('-'))
        # print(type(int(c[1:])))
                        if int(target[1][1:])>=int(code.split('-')[0][1:]) and int(target[1][1:])<=int(code.split('-')[1][1:]):
                            if target[3] in course[2]:
                                if  (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    return (True, 'open',course)
                                else:
                                    continue

                elif code=='xxx':
                    if target[0]+' '+target[1] not in course[4]:
                        if target[3] in course[2]:
                            if  (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                return (True, 'open',course)
                            else:
                                continue
                                # return (False, 'strict', course)
                       
                elif code.endswith('xx'):
                    if target[0]+' '+target[1] not in course[4]:
                        if code[0]==target[1][0]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    return (True, 'open',course)
                                else:
                                    continue
                                    #return (False, 'open',course)
                        else:
                            continue
                elif code==target[1]:
                    if target[3] in course[2]:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            return (True, 'open',course)
                        else:
                            return (False, 'strict', course)
                else:
                    continue


        elif next((s for s in req if 'SEDS' in s), None):
            found=next((s for s in req if 'SEDS' in s), None)
            if target[0] in seds:
                codes=found.split(' ')[1].split('/')
                for code in codes:
                    if code=='xxx':
                        if target[0]+' '+target[1] not in course[4]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                    
                                    return (True, 'open',course)
                                else:
                                    continue
                                    # return (False, 'strict', course)
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        
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
                                    
                                    return (True, 'open',course)
                                else:
                                    continue
                                    
                                    # return (False, 'strict', course)
                        
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        
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
                                    
                                    return (True, 'open',course)
                                else:
                                    continue
                                    
                                    # return (False, 'strict', course)
                        
                    elif code.endswith('xx'):
                        if target[0]+' '+target[1] not in course[4]:
                            if code[0]==target[1][0]:
                                if target[3] in course[2]:
                                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                        
                                        return (True, 'open',course)

                                    else:
                                        continue

            
        elif course[0]=='Social Sciences Elective':
            hum_soc_electives, soc_elective_courses=check_soc_elective(hum_soc,soc_elective,major)
            if target[0] in soc_elective_courses:
                if target[0]+' '+target[1] not in course[4]:
                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                        
                        return (True, 'open',course)
            else:
                for term in hum_soc_electives:
                    if int(target[5])>=int(term[0]):
                        if target[0]+' '+target[1] in term:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                
                                return (True, 'open',course)
                            else:
                                continue
                                
                                # return (False, 'strict', course)
                        elif any('xxx' in s for s in term):
                            for s in term:
                                if "xxx" in s:
                                    if target[0] in s:
                                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                            
                                            return (True, 'open',course)
                                        else:
                                            continue
                                            
                                            # return (False, 'strict', course)
                    else:
                        if ('General elective', '', '6', 'D', '') in course_req_open:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                
                                return (True, 'open',('General elective', '', '6', 'D', ''))
                            else:
        
                                return (False, 'open',('General elective', '', '6', 'D', ''))
                        

        elif course[0]=="Humanities elective":
            hum_soc_electives, hum_elective_courses, hum=check_hum_elective(hum_soc,hum_electives,major,humanities)
            if target[0] in hum_elective_courses:
                if target[0]+' '+target[1] not in course[4]:
                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                        
                        return (True, 'open',course)
            else:
                for term in hum:
                    if int(target[5])>=int(term[0]):
                        if target[0]+' '+target[1] in term:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                
                                return (True, 'open',course)
                            else:
                                continue
                                # return (False, 'strict', course)
                    
                for term in hum_soc:
                        if int(target[5])>=int(term[0]):
                            if target[0]+' '+target[1] in term:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    
                                    return (True, 'open',course)
                                else:
                                    continue
                                    # return (False, 'strict', course)
                            elif any('xxx' in s for s in term):
                                for s in term:
                                    if "xxx" in s:
                                        if target[0] in s:
                                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                                
                                                return (True, 'open',course)
                                            else:
                                                continue
                                                # return (False, 'strict', course)
                if target[0] in ['CHN','FRE','GER','KFL','KOR','PER','RFL','SPA'] or target[0]+' '+ target[1] in ['TUR 301','TUR 305', 'TUR 411', 'TUR 412']:
                    if int(target[5])<541:
                        if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                            
                            return (True, 'open',course)

        elif course[0] =='Open xxx' :
            if target[3] in course[2]:
                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                    
                    return (True, 'open',course)
                else:
                    return (False, 'open',course)
                
        elif course[0]=='General Elective':
            for term in general:
                if target[0]+' '+'xxx' in term:
                    if int(target[5])>=int(term[0]):
                        if target[0]+' '+target[1] not in course[4]:
                            if target[3] in course[2]:
                                if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                    
                                    return (True, 'open',course)
                                else:
                                    return (False, 'open',course)
                    else:
                        if ('Humanities elective', '', '6', 'D', '') in course_req_open:
                            if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
                                
                                return (True, 'open',('Humanities elective', '', '6', 'D', ''))
                            else:
                                return (False, 'open',('Humanities elective', '', '6', 'D', ''))

            if target[3] in course[2]:
                if target[0]+' '+target[1] not in course[4]:
                    if (target[4] in grades and (grades[target[4]] >= grades.get(course[3], 0))) or target[4]=='in progress' or target[4]=='P':
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


def search(course_req_open, course_req_strict,target, major,hum_soc,soc_elective,grades,seds,smg, hum_electives,humanities,general):
    result=find_in_strict(course_req_strict, target, grades)
    if result:
        return result
    else:
        result=find_in_open(course_req_open, target, major,hum_soc,soc_elective,grades,seds,smg, hum_electives,humanities,general)
        if result:
            return result
        else:
            return None
        