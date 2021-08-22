"""
create KML maps from the Vietnam THOR dataset

Thomas W Whittam
"""


import datetime
import re

import kml

import pandas as pd


def clean_date(datestr):
    """
    clean the date string from yyyymmdd to yyyy-mm-dd

    Args:
        datestr(str): string containing the date

    Returns:
        cleandate(str): if the date has been modified or is 'INVALID'
        datestr(str): if the date requires no modification as it is already
                      in the correct format
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


def create_map(outputfile, mtypes):
    """
    create a kml map

     -drop unwanted columns
     -create the placemark name of the aircraft flying the mission and its
      callsign if available
     -use the data from the mission as the placemark info that appears when
      you click on the placemark
     -each mission type is in its own folder

    Args:
        mtypes(dict): dict of pandas dataframes, keys are mission types values
                      are pandas dataframe of missions of that type
        outputfile(str): path to write kml file to
    """
    cols2drop = [
        'NUMWEAPONSJETTISONED', 'NUMWEAPONSRETURNED', 'RELEASEALTITUDE',
        'RELEASEFLTSPEED', 'TGTWEATHER', 'TGTID', 'TGTCLOUDCOVER',
        'TGTCONTROL', 'OPERATIONSUPPORTED', 'AIRFORCEGROUP', 'AIRFORCESQDN',
        'WEAPONTYPECLASS', 'WEAPONTYPEWEIGHT']
    kmlmap = kml.KMLOutputParser(outputfile)
    kmlmap.create_kml_header()
    kmlmap.open_folder('Vietnam War Air Missions - THOR dataset')
    for mtype in mtypes:
        kmlmap.open_folder(mtype)
        operations = mtypes[mtype]
        operations.drop(cols2drop, axis=1, inplace=True)
        for index, row in operations.iterrows():
            operation = row.to_dict()
            desc = kmlmap.format_kml_placemark_description(operation)
            if isinstance(operation['CALLSIGN'], str):
                pointname = '{}  {}'.format(
                    operation['VALID_AIRCRAFT_ROOT'], operation['CALLSIGN'])
            else:
                pointname = operation['VALID_AIRCRAFT_ROOT']
            kmlmap.add_kml_placemark(
                pointname, desc,
                str(operation['TGTLONDDD_DDD_WGS84']),
                str(operation['TGTLATDD_DDD_WGS84']),
                altitude='0', timestamp=operation['MSNDATE'])
        kmlmap.close_folder()
    kmlmap.close_folder()
    kmlmap.close_kml_file()
    kmlmap.write_kml_doc_file()


def split_by_mission_type(df):
    """
    get a list of all the unique mission types

    Args:
        df(pandas dataframe): the datafram to split

    Returns:
        bymissiontypes(dict): dict of pandas dataframes, keys are mission types
                              values are pandas dataframe of missions
                              of that type
    """
    bymissiontypes = {}
    missiontypes = df['MFUNC_DESC'].unique()
    for mtype in missiontypes:
        bymissiontypes[mtype] = df[df['MFUNC_DESC'] == mtype]
    return bymissiontypes


def linebacker2_map(lbdf):
    """
    map Operation Linebacker 2

    filter to missions:
    -flown by the United States
    -between 18 and 29 December 1972
    -between 104 and 108 degrees longitude
    -between 20 and 22 degrees latitude

    writes a CSV file of the matching missions

    Args:
        lbdf(pandas dataframe): dataframe to make map from
    """
    print('Creating map of Operation Linebacker 2 targets')
    missiondates = ['1972-12-' + str(x) for x in range(18, 30)]
    lbdf = lbdf[lbdf['MSNDATE'].isin(missiondates)]
    lbdf = lbdf[lbdf['COUNTRYFLYINGMISSION'] == 'UNITED STATES OF AMERICA']
    lbdf = lbdf[
        (lbdf['TGTLONDDD_DDD_WGS84'] >= 104) &
        (lbdf['TGTLONDDD_DDD_WGS84'] <= 108) &
        (lbdf['TGTLATDD_DDD_WGS84'] >= 20) &
        (lbdf['TGTLATDD_DDD_WGS84'] <= 22)]
    missiontypesorganised = split_by_mission_type(lbdf)
    create_map('Operation Linebacker 2.kml', missiontypesorganised)
    lbcsv = lbdf.to_csv(header=True)
    with open('Operation Linebacker 2.csv', 'w') as f:
        f.write(lbcsv)


def main():
    """
    main program code

    load dataset
    clean the mission dates
    remove missions with no LAT LON co-ords
    create the map
    """
    filename = 'thor_data_vietnam.csv'
    df = pd.read_csv(filename)
    df['MSNDATE'] = df['MSNDATE'].apply(clean_date)
    df = df[df.MSNDATE != 'INVALID']
    df["TGTLONDDD_DDD_WGS84"].fillna('NO CO-ORDS', inplace=True)
    df["TGTLATDD_DDD_WGS84"].fillna('NO CO-ORDS', inplace=True)
    df = df[
        (df["TGTLONDDD_DDD_WGS84"] != 'NO CO-ORDS') &
        (df["TGTLATDD_DDD_WGS84"] != 'NO CO-ORDS')]
    linebacker2_map(df)


if __name__ == '__main__':
    main()
