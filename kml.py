"""
a parser to generate Keyhole Markup Language (KML) for Google Earth
"""


class KMLOutputParser():
    """
    Class to parse KML into an output file.

    Attributes:
        kmldoc(list): list of strings to make up the doc.kml
        kmlfilepath(str): path to output KML file
        kmlheader(str): first part of a KML file
        placemarktemplate(str): template for a KML placemark (pin on map)
        lineplacemarktemplate(str): template for KML linestring (line on map)
        styletemplate(str): template for custom icons on placemarks
    """
    def __init__(self, kmlfilepath):
        self.kmldoc = []
        self.kmlfilepath = kmlfilepath
        self.kmlheader = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>Operations Map</name>
<open>1</open>"""
        self.placemarktemplate = """
<Placemark>
<name>%s</name>
<description>%s</description>
<TimeStamp>
<when>%s</when>
</TimeStamp>
<LookAt>
<longitude>%s</longitude>
<latitude>%s</latitude>
<altitude>%s</altitude>
<heading>-0</heading>
<tilt>0</tilt>
<range>500</range>
</LookAt>
<Point>
<altitudeMode>absolute</altitudeMode>
<coordinates>%s</coordinates>
</Point>
</Placemark>"""

    @staticmethod
    def format_kml_placemark_description(placemarkdict):
        """
        format html tags for inside a kml placemark from a dictionary

        Args:
            placemarkdict(dict): dictionary of information for a placemark

        Returns:
            description(str): the dictionary items formatted as HTML string
                              suitable to be in a KML placemark description
        """
        starttag = "<![CDATA["
        newlinetag = "<br  />\n"
        endtag = "]]>"
        descriptionlist = []
        descriptionlist.append(starttag)
        for item in placemarkdict:
            if isinstance(placemarkdict[item], dict):
                descriptionlist.append(newlinetag)
                descriptionlist.append(item.upper())
                descriptionlist.append(newlinetag)
                for subitem in placemarkdict[item]:
                    descriptionlist.append(str(subitem).upper())
                    descriptionlist.append(' - ')
                    descriptionlist.append(str(placemarkdict[item][subitem]))
                    descriptionlist.append(newlinetag)
                continue
            descriptionlist.append(str(item).upper())
            descriptionlist.append(' - ')
            descriptionlist.append(str(placemarkdict[item]))
            descriptionlist.append(newlinetag)
        descriptionlist.append(endtag)
        description = ''.join(descriptionlist)
        return description

    def create_kml_header(self):
        """
        Write the first part of the KML output file.
        This only needs to be called once at the start of the kml file.
        """
        self.kmldoc.append(self.kmlheader)

    def add_kml_placemark(self, placemarkname, description, lon, lat,
                          altitude='0', timestamp=''):
        """
        Write a placemark to the KML file (a pin on the map!)

        timestamp in the format '%Y-%m-%dT%H:%M:%SZ'

        Args:
            placemarkname(str): text that appears next to the pin on the map
            description(str): text that will appear in the placemark
            lon(str): longitude in decimal degrees
            lat(str): latitude in decimal degrees
            altitude(str): altitude in metres
            timestamp(str): time stamp in XML format
        """
        placemarkname = remove_invalid_chars(placemarkname)
        coords = lon + ',' + lat + ',' + altitude
        placemark = self.placemarktemplate % (
            placemarkname, description, timestamp, lon, lat,
            altitude, coords)
        self.kmldoc.append(placemark)

    def open_folder(self, foldername):
        """
        open a folder to store placemarks

        Args:
            foldername(str): the name of the folder
        """
        cleanfoldername = remove_invalid_chars(foldername)
        openfolderstr = "<Folder>\n<name>{}</name>".format(cleanfoldername)
        self.kmldoc.append(openfolderstr)

    def close_folder(self):
        """
        close the currently open folder
        """
        closefolderstr = "</Folder>"
        self.kmldoc.append(closefolderstr)

    def close_kml_file(self):
        """
        Write the end of the KML file.
        This needs to be called once at the end of the file
        to ensure the tags are closed properly.
        """
        endtags = "\n</Document></kml>"
        self.kmldoc.append(endtags)

    def write_kml_doc_file(self):
        """
        write the tags to the kml doc.kml file
        """
        with open(self.kmlfilepath, 'w') as kmlout:
            for kmltags in self.kmldoc:
                kmlout.write(kmltags)


def remove_invalid_chars(xmlstring):
    """
    remove invalid chars from a string

    Args:
        xmlstring(str): input string to clean

    Returns:
        cleanstring(str): return string with invalid chars replaced or removed
    """
    invalidchars = {'<': '&lt;', '>': '&gt;', '"': '&quot;',
                    '\t': '    ', '\n': ''}
    cleanstring = xmlstring.replace('&', '&amp;')
    for invalidchar in invalidchars:
        cleanstring = cleanstring.replace(
            invalidchar, invalidchars[invalidchar])
    return cleanstring
