def quick_look(df, col_name):
    '''
    Provides a quick look at a column of date in data frame
    
    parameter:
    ---
    col_name: name of column in df 
    
    output:
    ---
    sql query:
    
    plot:
    '''


    query = f'''SELECT 
                    {col_name} ,
                    COUNT({col_name}) as count
                FROM {df} 
                GROUP BY 
                    {col_name}
                ORDER BY 
                    {col_name}
                '''
    spark.sql(query).show()
    df_check = spark.sql(query)
    pdf_check = df_check.toPandas()

    pdf_check.plot(kind='bar', x=col_name,y='count', fontsize=20);