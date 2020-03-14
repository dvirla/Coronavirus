import numpy as np
import pandas as pd
import matplotlib.pyplot as plt;
import seaborn as sns
import plotly.express as px
import re

plt.style.use('ggplot')
px.defaults.template = 'plotly_dark'
plt.rcParams['figure.dpi'] = 100


class histogram():

    def __init__(self):
        filename_pattern = "novel-corona-virus-2019-dataset/time_series_covid_19_{}.csv"
        confirmed = pd.read_csv(filename_pattern.format('confirmed')).set_index(
            ['Province/State', 'Country/Region', 'Lat', 'Long'])
        recovered = pd.read_csv(filename_pattern.format('recovered')).set_index(
            ['Province/State', 'Country/Region', 'Lat', 'Long'])
        deaths = pd.read_csv(filename_pattern.format('deaths')).set_index(
            ['Province/State', 'Country/Region', 'Lat', 'Long'])
        self.covid = pd.concat([pd.read_csv(filename_pattern.format(name.lower()))
                               .melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                     var_name='Date', value_name=name)
                                .set_index(['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])

        for name in ['Confirmed', 'Recovered', 'Deaths']], axis=1).reset_index()\
            .assign(Infected=lambda df: df['Confirmed']-df['Recovered']-df['Deaths'])
        self.covid['Date'] = pd.to_datetime(self.covid['Date'])
        self.covid['Country/Region'] = self.covid['Country/Region'].replace({
                                                                            'Mainland China': 'China',
                                                                            'Republic of Korea': 'Korea, South',
                                                                            'Iran (Islamic Republic of)': 'Iran', })
        self.covid_world = self.covid.groupby('Date')[['Confirmed', 'Recovered', 'Deaths', 'Infected']].sum()
        # print total numbers
        # print(self.covid_world.iloc[[-1]])

        # plot line of current totals
        # df = self.covid_world.reset_index().melt(id_vars='Date', var_name='Status', value_name='Subjects')
        # fig = px.line(df, 'Date', 'Subjects', color='Status', title='World wide trends')
        # fig.show()

        # print rates of recovery and death
        # print(self.covid_world.iloc[[-1]].assign(
        #     RecoveryRate=lambda df: df['Recovered'] / df['Confirmed'],
        #     DeathRate=lambda df: df['Deaths'] / df['Confirmed']))

        # print confirmed by country from largest to smallest
        country = confirmed.groupby(['Country/Region']).sum()
        latest_confirmed = country[country.columns[-1]].sort_values(ascending=False).astype(int).to_frame(
             'Confirmed').reset_index()
        # latest_confirmed_updated = latest_confirmed.nlargest(20, 'Confirmed')
        # print(latest_confirmed_updated)
        # fig = px.bar(latest_confirmed.nlargest(20, 'Confirmed'), x='Country/Region', y='Confirmed')
        # fig.show()

        covid_countries = self.covid.groupby(['Country/Region', 'Date'])[
            'Confirmed', 'Recovered', 'Deaths', 'Infected'].sum()

        covid_countries_long = covid_countries.reset_index().melt(id_vars=['Date', 'Country/Region'], var_name='Status',
                                                                  value_name='Subjects')

        top_countries = covid_countries_long[(covid_countries_long['Country/Region'].isin(
            latest_confirmed.nlargest(10, 'Confirmed')['Country/Region'][1:])) &
                                             (covid_countries_long['Status'] == 'Confirmed')] \
            .rename({'Subjects': 'Confirmed'}, axis=1)

        fig = px.scatter(top_countries, 'Date', 'Confirmed', color='Country/Region',
                         log_y=True, height=600)
        fig.update_traces(mode='lines+markers', line=dict(width=.5))
        fig.update_layout(title='Exponential growth in the top ten most-affected countries (except China)')

        # showing top ten countries with daily differences
        # diffs = covid_countries.reset_index().groupby('Country/Region') \
        #     .apply(lambda g: g.sort_values('Date').assign(Diff=g['Infected'].diff())).reset_index(drop=True)
        # countries = [c for c in self.covid['Country/Region'].unique()
        #              if re.search(r'China|Korea, South|Italy|Iran|US|Israel', c)]
        # fig = px.line(diffs[diffs['Country/Region'].isin(countries)], x='Date', y='Diff', color='Country/Region')
        fig.show()