import tkinter as tk
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import xlsxwriter


class CrawlLiveScores():
    """
    Class: fetches football scores from livescores.com within
            a specified time interval (7 days)
    """

    URL_ = "http://www.livescores.com/soccer/"

    def __init__(self):
        self.endtime = dt.date.today()
        self.starttime = self.endtime - dt.timedelta(days=7)
        filename_startdate = self.starttime.strftime("%m_%d_%Y")
        filename_enddate = self.endtime.strftime("%m_%d_%Y")
        self.starttime = self.starttime.strftime("%m/%d/%Y")
        self.endtime = self.endtime.strftime("%m/%d/%Y")
        self.test = "1_111"
        self.filename = f"teamscores-{filename_startdate}-{filename_enddate}"
        self.save_to_excel()

    def prepare_dates(self):
        self.daterange = pd.date_range(
            start=self.starttime,
            end=self.endtime
        ).astype(str)
        return self.daterange

    def save_to_excel(self):
        with pd.ExcelWriter(f"{self.filename}.xlsx", engine="xlsxwriter") as writer:
            for i in range(len(self.prepare_dates())):
                date_i = self.prepare_dates()[i]
                footdates = f"{self.URL_}{date_i.split(' ')[0]}"
                webdata = requests.get(footdates)
                soup = BeautifulSoup(webdata.content, 'lxml')
                find_home_team = soup.findAll(class_='ply tright name')
                find_scores = soup.findAll(class_='sco')
                find_away_team = soup.findAll(class_='ply name')

                home_team = [date_i.text for date_i in find_home_team]
                scores = [date_i.text for date_i in find_scores]
                away_team = [date_i.text for date_i in find_away_team]
                df = pd.DataFrame({})
                df['Home Team'] = home_team
                df['Scores'] = scores
                df['Away Team'] = away_team
                df.to_excel(
                    writer,
                    index=False,
                    sheet_name=date_i.split(" ")[0]
                )
            writer.save()


root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()


def cls():

    if __name__ == '__main__':
        CrawlLiveScores()


button1 = tk.Button(text='Show Result', command=cls, bg='brown', fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()