import zipfile
import tempfile
import xml.etree.ElementTree as etree
import io
import shutil
import os


def get_metadata(filepath):
    """Return Comics Metadata as Dictionary"""
    def get_full_series():
        series = root.findtext('Series')
        number = root.findtext('Number')
        title = root.findtext('Title')

        if series and number and title:
            series = series + ' ' + number + ' ' + title
        elif series and number and not title:
            series = series + ' ' + number
        elif series and not number and title:
            series = series + ' ' + title
        else:
            series = series
        return series

    def get_writer():
        try:
            writer = root.findtext('Writer').split(', ')
        except:
            writer = []
        return writer

    def get_penciller():
        try:
            penciller = root.findtext('Penciller').split(', ')
        except:
            penciller = []
        return penciller

    def get_genre():
        try:
            genre = root.findtext('Genre').split(', ')
        except:
            genre = []
        return genre

    def get_year():
        try:
            year = root.findtext('Year')
        except:
            year = ''
        return year

    def get_month():
        try:
            month = root.findtext('Month')
        except:
            month = ''
        return month

    def get_day():
        try:
            day = root.findtext('Day')
        except:
            day = ''
        return day

    metadata = {}

    with zipfile.ZipFile(filepath, mode='r',) as z:
        try:
            comicinfoxml = z.open('ComicInfo.xml', mode='r')
            infotree = etree.parse(comicinfoxml)
            root = infotree.getroot()
            metadata['Series'] = get_full_series()
            metadata['Writer'] = get_writer()
            metadata['Penciller'] = get_penciller()
            metadata['Genre'] = get_genre()
            metadata['Year'] = get_year()
            metadata['Month'] = get_month()
            metadata['Day'] = get_day()

            return metadata
        except:
            raise


def write_metadata(filepath, metadata):
    """Write metadata to Comic Archive"""

    def generate_xml():
        """Generate ComicInfo.xml to Write"""
        g = io.StringIO()

        with zipfile.ZipFile(filepath, mode='r',) as z:

            comicinfoxml = z.open('ComicInfo.xml', mode='r')
            infotree = etree.parse(comicinfoxml)
            root = infotree.getroot()

            try:
                root.remove(root.find('Number'))
            except:
                pass
            try:
                root.remove(root.find('Title'))
            except:
                pass
            for k, v in metadata.items():
                if (v != '') & (root.find(k) is not None):
                    root.find(k).text = v
                elif (v != '') & (root.find(k) is None):
                    newelement = etree.Element(k)
                    newelement.text = v
                    root.append(newelement)
                elif v == '':
                    try:
                        root.remove(root.find(k))
                    except:
                        print('remove failed')
            infotree.write(g, encoding='unicode')

        return g

    gx = generate_xml()

    remove_comicinfo_from_zip(filepath)

    with zipfile.ZipFile(filepath, mode='a',) as z:
        z.writestr('ComicInfo.xml', gx.getvalue())


def remove_comicinfo_from_zip(filepath):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(filepath, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename != 'ComicInfo.xml':
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, filepath)
    finally:
        shutil.rmtree(tempdir)