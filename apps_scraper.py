from google_play_scraper import app
from google_play_scraper import Sort, reviews_all
from app_store_scraper import AppStore
import pprint as pp
import pandas as pd

column_names = ["Store", "appId", "Title",
                "Total_Score", "Ratings", "Installs", "Reviews",
                "Released", "Developer", "Genre", "containsAds", "Free",
                "User_Comments_EN", "User_Scores_EN", "User_Dates_EN", "User_Helpful_Thumb_EN",
                "User_Comments_PL", "User_Scores_PL", "User_Dates_PL", "User_Helpful_Thumb_PL"]

scrapped_df_google = pd.DataFrame(columns = column_names)
scrapped_df_apple = pd.DataFrame(columns = column_names)


# Apple App Store

research_df = pd.read_excel('research.xlsx', usecols="B, C", sheet_name='Apple')

for row_count in range(research_df.shape[0]):

    # scraping general info with BeautifulSoup


    # scraping reviews

    application = AppStore(country="us", app_name=research_df['app_name'].iloc[row_count], app_id=research_df['app_id'].iloc[row_count])
    application.review(how_many=100)

    user_comments_en = []
    user_scores_en = []
    user_dates_en = []

    for user in application.reviews:
        user_comments_en.append(user['review'])
        user_scores_en.append(user['rating'])
        user_dates_en.append(user['date'])

    application = AppStore(country="pl", app_name=research_df['app_name'].iloc[row_count], app_id=research_df['app_id'].iloc[row_count])
    application.review(how_many=100)

    user_comments_pl = []
    user_scores_pl = []
    user_dates_pl = []

    for user in application.reviews:
        user_comments_pl.append(user['review'])
        user_scores_pl.append(user['rating'])
        user_dates_pl.append(user['date'])

    scrapped_df_apple.loc[row_count] = ['Apple App Store',
                                       #  research_df['app_id'].iloc[row_count], <- zmienic
                                       #  general_info['title'],
                                       #  general_info['score'],
                                       #  general_info['ratings'],
                                       #  general_info['installs'], <- chyba N/A
                                       #  general_info['reviews'], <- chyba N/A
                                       #  general_info['released'], <- chyba N/A
                                       #  general_info['developer'],
                                       #  general_info['genre'], <- chyba N/A
                                       #  general_info['containsAds'], <- chyba N/A
                                       #  general_info['free'],
                                         user_comments_en,
                                         user_scores_en,
                                         user_dates_en,
                                         'N/A',
                                         user_comments_pl,
                                         user_scores_pl,
                                         user_dates_pl,
                                         'N/A']


# scrapped_df_apple.to_excel("scrapped.xlsx")
# scrapped_df_apple.to_hdf('scrapping.hd5', key='s', mode='w')
# scrapped_df_apple = pd.read_hdf('scrapping.h5', key='s')


# Google Play Store

research_df = pd.read_excel('research.xlsx', usecols="B", sheet_name='Google')

for row_count in range(research_df.shape[0]):

    general_info = app(
        research_df['Id'].iloc[row_count],
        lang='en',
        country='EU'
    )

    result_en = reviews_all(
        research_df['Id'].iloc[row_count],
        sleep_milliseconds=0,  # defaults to 0
        lang='en',
        country='EU',
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=5  # defaults to None(means all score)
    )

    result_pl = reviews_all(
        research_df['Id'].iloc[row_count],
        sleep_milliseconds=0,  # defaults to 0
        lang='pl',
        country='EU',
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=5  # defaults to None(means all score)
    )

    user_comments_en = []
    user_scores_en = []
    user_dates_en = []
    user_helpful_thumbs_en = []

    for user in result_en:
        user_comments_en.append(user['content'])
        user_scores_en.append(user['score'])
        user_dates_en.append(user['at'])
        user_helpful_thumbs_en.append(user['thumbsUpCount'])

    user_comments_pl = []
    user_scores_pl = []
    user_dates_pl = []
    user_helpful_thumbs_pl = []

    for user in result_pl:
        user_comments_pl.append(user['content'])
        user_scores_pl.append(user['score'])
        user_dates_pl.append(user['at'])
        user_helpful_thumbs_pl.append(user['thumbsUpCount'])


    scrapped_df_google.loc[row_count] = ['Google Play Store',
                                  research_df['Id'].iloc[row_count],
                                  general_info['title'],
                                  general_info['score'],
                                  general_info['ratings'],
                                  general_info['installs'],
                                  general_info['reviews'],
                                  general_info['released'],
                                  general_info['developer'],
                                  general_info['genre'],
                                  general_info['containsAds'],
                                  general_info['free'],
                                  user_comments_en,
                                  user_scores_en,
                                  user_dates_en,
                                  user_helpful_thumbs_en,
                                  user_comments_pl,
                                  user_scores_pl,
                                  user_dates_pl,
                                  user_helpful_thumbs_pl]




# scrapped_df_google.to_excel("scrapped.xlsx")
# scrapped_df_google.to_hdf('scrapping.hd5', key='s', mode='w')
# scrapped_df_google = pd.read_hdf('scrapping.h5', key='s')





