import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re

class sarsreader():
    def __init__(self):
        file_path = "sars-outbreak-2003-complete-dataset/sars_2003_complete_dataset_clean.csv"
        self.cases_by_dates = pd.read_csv(file_path)
        self.totals_per_state = self.cases_by_dates.groupby('Country')[['Cumulative number of case(s)',
                                                              'Number of deaths', 'Number recovered']].sum()
        self.sars_world = self.cases_by_dates.sum(numeric_only=True)

    def recov_death_rates(self):
        print("Recovery Rate = ", self.sars_world['Number recovered']/ self.sars_world['Cumulative number of case(s)'])
        print("Death Rate=", self.sars_world['Number of deaths'] / self.sars_world['Cumulative number of case(s)'])