from app_store_scraper import AppStore
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


column_names = ["Store", "appId", "Title",
                "Total_Score", "Ratings", "Installs", "Reviews_Count",
                "Released", "Developer", "containsAds", "Free",
                "User_Comments_PL", "User_Scores_PL", "User_Dates_PL"]

scrapped_df_apple = pd.DataFrame(columns = column_names)

research_df = pd.read_excel('research.xlsx', usecols="B, C:D", sheet_name='Apple')


for row_count in range(research_df.shape[0]):

    # scraping general info with BeautifulSoup

    url = research_df['url PL'].iloc[row_count]
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")


    title = doc.find(class_="product-header__title app-header__title")
    age = doc.find(class_="badge badge--product-title")
    title = title.text
    title = title.split(age.text)
    title = title[0]
    title = title.strip()

    reg_score = re.compile(r'^(.*?) •')
    score = doc.find(class_="we-rating-count star-rating__count")
    score = re.findall(reg_score, score.text)
    score = score[0]

    reg_ratings = re.compile(r':.*')
    ratings = doc.find(class_="we-rating-count star-rating__count")
    ratings = re.findall(reg_ratings, ratings.text)
    ratings = ratings[0].strip(': ')

    developer = doc.find(class_="product-header__identity app-header__identity")
    developer = developer.text.strip()

    free = doc.find(class_="inline-list__item inline-list__item--bulleted app-header__list__item--price")
    if free.text == 'Gratis':
        free = 'True'
    else:
        free = 'False'


    # scraping reviews


    application = AppStore(country="pl", app_name=research_df['app_name'].iloc[row_count],
                                       app_id=research_df['app_id'].iloc[row_count])
    application.review(how_many=100)


    user_comments_pl = []
    user_scores_pl = []
    user_dates_pl = []

    for user in application.reviews:
        user_comments_pl.append(user['review'])
        user_scores_pl.append(user['rating'])
        user_dates_pl.append(user['date'])

    reviews_count = len(user_comments_pl)

    scrapped_df_apple.loc[row_count] = ['Apple App Store',
                                         research_df['app_id'].iloc[row_count],
                                         title,
                                         score,
                                         ratings,
                                         'N/A', # <- installs
                                         reviews_count,
                                         'N/A', # <- released
                                         developer,
                                         'N/A', # <- containsAds
                                         free,
                                         user_comments_pl,
                                         user_scores_pl,
                                         user_dates_pl]


scrapped_df_apple.to_hdf('scrapping.hd5', key='s', mode='w')