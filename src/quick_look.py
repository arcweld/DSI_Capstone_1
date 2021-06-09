def ql(df, col_name):
    '''
    Provides a quick look at a column of date in data frame
    
    parameter:
    ---
    col_name: name of column in df 
    
    output:
    ---
    sql query:
    
    '''
    return f'''SELECT 
                    {col_name} ,
                    COUNT({col_name}) as count
                FROM {df} 
                GROUP BY 
                    {col_name}
                ORDER BY 
                    {col_name}
                '''


def quick_plot(df, col_name):
    return df.plot(kind='bar', x=col_name, y='count', fontsize=20);