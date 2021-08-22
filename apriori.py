"""
Use the Apriori Algorithm on the Vietnam War THOR dataset

Thomas Whittam
"""


import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder


def main():
    """
    main program code
    """
    filename = 'thor_data_vietnam.csv'
    cols2process = [
        'MILSERVICE', 'VALID_AIRCRAFT_ROOT', 'TGTTYPE',
        'MFUNC_DESC', 'TGTCOUNTRY', 'WEAPONTYPE', 'MFUNC_DESC_CLASS']
    df = pd.read_csv(filename, usecols=cols2process)
    df = df[df['MFUNC_DESC_CLASS'] == 'KINETIC']
    df = df.drop(['MFUNC_DESC_CLASS'], axis=1)
    cleandf = df.dropna()
    preparedlist = cleandf.values.tolist()

    te = TransactionEncoder()
    te_ary = te.fit(preparedlist).transform(preparedlist)
    df2 = pd.DataFrame(te_ary, columns=te.columns_)

    results = apriori(df2, min_support=0.1, use_colnames=True)
    print(results)


if __name__ == '__main__':
    main()
