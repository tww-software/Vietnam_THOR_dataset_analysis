"""
tally up the values of the fields we are interested in
and save to CSV

Vietnam War THOR Dataset

Thomas Whittam
"""


import pandas as pd


FIELDS = {
    'Military Service': 'MILSERVICE',
    'Aircraft Type': 'VALID_AIRCRAFT_ROOT',
    'Take Off Location': 'TAKEOFFLOCATION',
    'Target Type': 'TGTTYPE',
    'Mission Type': 'MFUNC_DESC',
    'Target Country': 'TGTCOUNTRY',
    'Country Flying Misson': 'COUNTRYFLYINGMISSION',
    'Kinetic OR Non Kinetic': 'MFUNC_DESC_CLASS',
    'Unit': 'UNIT',
    'Weapon Type': 'WEAPONTYPE',
    'Mission Date': 'MSNDATE'}


def frequency_tables(df):
    """
    generate frequency tables for:
      mission type to whether mission is Kinetic or Non Kinetic
      aircraft type to mission type

    Args:
        df(pandas dataframe): dataframe to make frequency tables from
    """
    print('creating mission type to Kinetic/Non Kinetic frequency table')
    missiontype2kinetic = pd.crosstab(df.MFUNC_DESC, df.MFUNC_DESC_CLASS)
    missiontype2kineticcsv = missiontype2kinetic.to_csv(header=True)
    with open('missiontype_to_kinetic_frequency_table.csv', 'w') as f:
        f.write(missiontype2kineticcsv)
    print('creating aircraft type to mission type frequency table')
    aircraft2mission = pd.crosstab(df.VALID_AIRCRAFT_ROOT, df.MFUNC_DESC)
    aircraft2missioncsv = aircraft2mission.to_csv(header=True)
    with open('aircrafttype_to_missiontype_frequency_table.csv', 'w') as f2:
        f2.write(aircraft2missioncsv)


def main():
    """
    main program code
    """
    filename = 'thor_data_vietnam.csv'
    df = pd.read_csv(filename)
    for field in FIELDS:
        print('counting values for - {}'.format(field))
        count = df.groupby(FIELDS[field]).size()
        header = '{},Count\n'.format(field)
        countcsv = count.to_csv()
        with open(field + '-tally.csv', 'w') as f:
            f.write(header)
            f.write(countcsv)
    frequency_tables(df)


if __name__ == '__main__':
    main()
