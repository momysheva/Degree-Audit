basic=['KAZ 150', 'KAZ 201', 'KAZ 202', 'KAZ 3xx']
intermediate=[ 'KAZ 201', 'KAZ 202', 'KAZ 3xx']
upper_intermediate=['KAZ 202', 'KAZ 3xx']
advanced=['KAZ 3xx', 'KAZ 3xx']
foreign=['KFL 101', 'KFL 102', 'KFL 201', 'KFL 202']


def check_kaz_level(kaz_courses):
    kaz=kaz_courses[0]
    if kaz[0]+' '+ kaz[1]==foreign[0]:
        level='foreign'
    elif kaz[0]+' '+ kaz[1]==basic[0]:
        level='basic'
    elif kaz[0]+' '+ kaz[1]==intermediate[0]:
        level='intermediate'
    elif kaz[0]+' '+ kaz[1]==upper_intermediate[0]:
        level='upper-intermediate'
    else:
        level='advanced'
    return level







    
    