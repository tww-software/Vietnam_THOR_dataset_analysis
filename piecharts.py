"""
generate pie charts
from the Vietnam War THOR dataset

Thomas Whittam
"""


import pandas as pd
import matplotlib.pyplot as plt


def pie_chart_maker(outputfilename, dataframe, catagory, title):
    """
    generate pie charts for a column in the dataframe by tallying up the values

    Args:
        outputfilename(str): filename to save the pie chart as
        dataframe(pandas dataframe): the raw data in a pandas dataframe
        catagory(str): the column we want to tally up and make a pie chart from
        title(str): title to appear on the chart
    """
    count = dataframe.groupby([catagory]).size()
    countdict = count.to_dict()
    countdict = dict(sorted(countdict.items(), key=lambda x: x[1]))
    labels = list(countdict.keys())
    values = list(countdict.values())
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.pie(values, labels=labels, autopct='%1.1f%%', rotatelabels=True)
    plt.title(title)
    plt.savefig(outputfilename)
    plt.clf()


def main():
    """
    main program code
    """
    catagories = {
        'Military Service': 'MILSERVICE',
        'Aircraft Type': 'VALID_AIRCRAFT_ROOT',
        'Take Off Location': 'TAKEOFFLOCATION',
        'Target Type': 'TGTTYPE',
        'Mission Type': 'MFUNC_DESC',
        'Target Country': 'TGTCOUNTRY'}
    filename = 'thor_data_vietnam.csv'
    df = pd.read_csv(filename)
    for catagory in catagories:
        print('creating pie chart for - {}'.format(catagory))
        outfile = '{}_{}_pie.png'.format(filename, catagory)
        pie_chart_maker(outfile, df, catagories[catagory], catagory)


if __name__ == '__main__':
    main()
