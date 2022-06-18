from google_play_scraper import app
from google_play_scraper import Sort, reviews_all
import pandas as pd


column_names = ["Store", "appId", "Title",
                "Total_Score", "Ratings", "Installs", "Reviews_Count",
                "Released", "Developer", "containsAds", "Free",
                "User_Comments_PL", "User_Scores_PL", "User_Dates_PL"]

scrapped_df_google = pd.DataFrame(columns = column_names)

research_df = pd.read_excel('research.xlsx', usecols="B", sheet_name='Google')


for row_count in range(research_df.shape[0]):

    general_info = app(
        research_df['Id'].iloc[row_count],
        lang='pl',
        country='PL'
    )

    result_pl = reviews_all(
        research_df['Id'].iloc[row_count],
        sleep_milliseconds=0,  # defaults to 0
        lang='pl',
        country='PL',
        sort=Sort.MOST_RELEVANT,
        filter_score_with=None
    )

    user_comments_pl = []
    user_scores_pl = []
    user_dates_pl = []

    for user in result_pl:
        user_comments_pl.append(user['content'])
        user_scores_pl.append(user['score'])
        user_dates_pl.append(user['at'])


    scrapped_df_google.loc[row_count] = ['Google Play Store',
                                  research_df['Id'].iloc[row_count],
                                  general_info['title'],
                                  general_info['score'],
                                  general_info['ratings'],
                                  general_info['installs'],
                                  general_info['reviews'],
                                  general_info['released'],
                                  general_info['developer'],
                                  general_info['containsAds'],
                                  general_info['free'],
                                  user_comments_pl,
                                  user_scores_pl,
                                  user_dates_pl]




scrapped_df_google.to_hdf('scrapping.hd5', key='s', mode='w')






