"""
create Time Series graphs from the Vietnam War THOR dataset

Thomas Whittam
"""

import datetime
import re

import pandas as pd
import matplotlib.pyplot as plt


def clean_date(datestr):
    """
    clean the date string from yyyymmdd to yyyy-mm-dd
    """
    datestr = str(datestr)
    if re.match(r'^(\d{8})', datestr):
        cleandate = '{}-{}-{}'.format(datestr[0:4], datestr[4:6], datestr[6:9])
        try:
            datetime.date(
                int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:9]))
        except ValueError:
            cleandate = 'INVALID'
        return cleandate
    else:
        return datestr


def single_time_series(outputfilename, count, title):
    """
    generate time series line chart

    Args:
        outputfilename(str): filename to save the pie chart as
        dataframe(pandas.core.series.Series): the raw data in a pandas series
        title(str): chart title
    """
    countdict = count.to_dict()
    dates = list(countdict.keys())
    missions = list(countdict.values())
    plt.figure(figsize=(25, 10))
    plt.plot_date(x=dates, y=missions, linestyle='solid')
    plt.title(title)
    plt.xlabel("Dates")
    plt.ylabel("No of Missions per day")
    plt.savefig(outputfilename)
    plt.clf()


def multiple_time_series(outputfilename, seriesdict, title):
    """
    generate time series line chart with multiple lines

    Args:
        outputfilename(str): filename to save the pie chart as
        seriesdict(dict): dictionary of counts to plot key is name, value is
                          the series data to plot as a line on the graph
        title(str): chart title
    """
    plt.figure(figsize=(25, 10))
    for line in seriesdict:
        countdict = seriesdict[line].to_dict()
        dates = list(countdict.keys())
        missions = list(countdict.values())
        plt.plot_date(x=dates, y=missions, linestyle='solid', label=line)
    plt.title(title)
    plt.legend()
    plt.xlabel("Dates")
    plt.ylabel("No of Missions per day")
    plt.savefig(outputfilename)
    plt.clf()


def main():
    """
    main program code
    """
    filename = 'thor_data_vietnam.csv'
    df = pd.read_csv(filename)
    print('calculating time series for entire war')
    df['MSNDATE'] = df['MSNDATE'].apply(clean_date)
    df = df[df.MSNDATE != 'INVALID']
    df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%Y-%m-%d')
    count = df.groupby(['MSNDATE']).size()
    single_time_series(
        'timeseries.png', count,
        'Missions per day, Vietnam War (1965-1975) Total')
    print('calculating time series for target countries')
    northvietnam = df[df['TGTCOUNTRY'] == 'NORTH VIETNAM']
    nvcount = northvietnam.groupby(['MSNDATE']).size()
    southvietnam = df[df['TGTCOUNTRY'] == 'SOUTH VIETNAM']
    svcount = southvietnam.groupby(['MSNDATE']).size()
    laos = df[df['TGTCOUNTRY'] == 'LAOS']
    lcount = laos.groupby(['MSNDATE']).size()
    cambodia = df[df['TGTCOUNTRY'] == 'CAMBODIA']
    ccount = cambodia.groupby(['MSNDATE']).size()
    targetcountry = {'North Vietnam': nvcount,
                     'South Vietnam': svcount,
                     'Laos': lcount,
                     'Cambodia': ccount}
    multiple_time_series(
        'target country time series.png', targetcountry,
        'Missions per day, Vietnam War (1965-1975) per Target Country')
    print('calculating time series for allied countries')
    australia = df[df['COUNTRYFLYINGMISSION'] == 'AUSTRALIA']
    auscount = australia.groupby(['MSNDATE']).size()
    southkorea = df[df['COUNTRYFLYINGMISSION'] == 'KOREA (SOUTH)']
    skcount = southkorea.groupby(['MSNDATE']).size()
    laos2 = df[df['COUNTRYFLYINGMISSION'] == 'LAOS']
    l2count = laos2.groupby(['MSNDATE']).size()
    usa = df[df['COUNTRYFLYINGMISSION'] == 'UNITED STATES OF AMERICA']
    usacount = usa.groupby(['MSNDATE']).size()
    southvietnam2 = df[df['COUNTRYFLYINGMISSION'] == 'VIETNAM (SOUTH)']
    sv2count = southvietnam2.groupby(['MSNDATE']).size()
    countryflying = {'Australia': auscount,
                     'South Vietnam': sv2count,
                     'Laos': l2count,
                     'South Korea': skcount,
                     'United States of America': usacount}
    multiple_time_series(
        'flying country time series.png', countryflying,
        'Missions per day, Vietnam War (1965-1975) per Country Flying Mission')


if __name__ == '__main__':
    main()
