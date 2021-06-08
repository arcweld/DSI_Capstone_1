import re


def dd_to_structure(dd_path):
    '''
    Harvests from a US Census Bureau data dictionary the headings, lengths, and locations of fixed-width elements.
    
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
    '''
    structure = r'' # tmp_df.value.substr([position],[length]).alias('colname')
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
                    last_loc = int(loc[0][0])

