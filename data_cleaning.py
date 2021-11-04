

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
df['min_slalry']=df.apply(lambda x: x.min_salary*2 if x.hourly==1 else x.min_salary,axis=1)
df['max_salary'] = df.apply(lambda x: x.max_salary*2 if x.hourly ==1 else x.max_salary, axis =1)
df['avg_salary']=(df.min_salary+df.max_salary)/2

#Company name text only
df['company_txt']=df.apply(lambda x:x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)
df['company_txt'] = df.company_txt.apply(lambda x: x.replace('\n', ''))

#state field
#df['job_state']=df['Location'].apply(lambda x: x.split(',')[1] if x!='Remote' else x)
df['job_state']=df['Location'].apply(lambda x :"Remote" if x=='Remote' else("-1" if x=="United States" else ("NY" if x=="New York State" else x.split(',')[1])))
df['remote']=df['Location'].apply(lambda x: 1 if x=='Remote' else 0)

df['age'] = df.Founded.apply(lambda x: int(-1) if x in('-1','Company - Private','Company - Public','Government','Contract','Unknown') else 2021 - int(x))

#parsing of job description(python,etc.)
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower() or 'junior' in title.lower():
        return 'jr'
    else:
        return 'na'
    
df['job_simp']=df['Job Title'].apply(title_simplifier)

df['seniority']=df['Job Title'].apply(seniority)
df.seniority.value_counts()

df['desc_len'] = df['Job Description'].apply(lambda x: len(x))

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



df.to_csv('salary_data_cleaned.csv',index = False)
