import re


def dd_to_structure(dd_path):
    '''Decompose a US Census Bureau data dictionary 
    for needed info on fixed-width elements.
    
    parameter:
    -----
    dd_path: string
        relative or absolute path to data dictionary. 
        
    output: 
    -----
    headers: list of strings
        name of each column from data dictionary
    locations: list of tuples
        first and last index for each column in data dictionary
    sizes: list of integers
        width of each column in data dictionary
    structures: string
        
    '''
    structure = r'' # tmp_df.value.substr([position],[length]).alias('colname')
    headers = []
    locations = []
    sizes = []
    last_loc = -1
    with open(dd_path, 'r') as d:
            data_dict = d.readlines()

    for line in data_dict:
        header = re.findall("\A([A-Z0-9]*)\s", line)
        loc = re.findall("(\d+)\s*-\s*(\d+)$", line)
        size = re.findall("\A[A-Z0-9]+\s+(\d+)", line)
        if header != []:
            if size != []:
                if loc != []: # and int(loc[0][1])>last_loc and int(loc[0][1])<1900:
    #                 structure[header] = f"tmp_df.value.substr({int(loc[0][0])}, {int(size[0])}).alias('{header}')"
                    if header[0] == 'FILLER':
                        header[0] = f'FILLER{int(loc[0][0])}'
                    if header[0] == 'PADDING':
                        header[0] = f'PADDING{int(loc[0][0])}'
                    structure += f"tmp_df.value.substr({int(loc[0][0]):>2}, {int(size[0]):>2}).alias('{header[0]}'), "
                    headers.append(header[0])
                    locations.append((int(loc[0][0]),int(loc[0][1])))
                    sizes.append(int(size[0]))
                    last_loc = int(loc[0][0])


    return headers, locations, sizes, structure


def ageGrouping(age_):
    age = int(age_)
    if age >= 0 and age <= 20:
        return ' U21'
    if age > 20  and age <= 30:
        return '21-30'
    if age > 30  and age <= 40:
        return '31-40'
    if age > 40  and age <= 50:
        return '41-50'
    if age > 50  and age <= 60:
        return '51-60'
    if age > 60  and age <= 70:
        return '61-70'
    if age > 70:
        return 'over_70'
    return '  None'
