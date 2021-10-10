if __name__ == '__main__':
    import glassdoor_scrapper as gs
    from selenium import webdriver
    import pandas as pd

    #path = "D:|DS|projects|ds_salary|chromedriver"
    df = gs.get_jobs('data scientist', 15, False)
    df

