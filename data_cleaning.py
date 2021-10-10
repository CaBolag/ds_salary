# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 13:52:40 2021

@author: Victor
"""

import pandas as pd
df=pd.read_csv('glassdoor_jobs.csv')

#salary parsing

df['hourly']=df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided']=df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)
df['Salary Estimate']=df['Salary Estimate'].apply(lambda x: x if '-' in x else '-1')
df=df[df['Salary Estimate']!='-1']

salary=df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd=salary.apply(lambda x: x.replace('K','').replace('$',''))
min_hr=minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary']=min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary']=min_hr.apply(lambda x: int(x.split('-')[1]))
df['avr_salary']=(df.min_salary+df.max_salary)/2

#Company name text only
df['company_txt']=df.apply(lambda x:x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)

#state field
df['job_state']=df['Location'].apply(lambda x: x.split(',')[1] if x!='Remote' else x)
#df['same_state']=df.apply(lambda x: 1 if x.Location==x.He)

df['age'] = df.Founded.apply(lambda x: int(-1) if x in('-1','Company - Private','Company - Public','Government') else 2021 - int(x))

#parsing of job description(python,etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
#r studio 
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark 
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws 
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df_out=df.to_csv('salary_data_cleaned.csv',index = False)
