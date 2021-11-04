if __name__ == '__main__':
    import glassdoor_scrapper as gs
    from selenium import webdriver
    import pandas as pd

    #path = "D:|DS|projects|ds_salary|chromedriver"
    df = gs.get_jobs('data scientist', 2000, False)
    df.to_csv('glassdoor_jobs.csv',index=False)
    

