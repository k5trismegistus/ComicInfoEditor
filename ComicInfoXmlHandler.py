import zipfile
import xml.etree.ElementTree as etree



class ComicInfoXmlHandler():

    def __init__(self, fromxml):
        self.fromxml = fromxml
        self.todisplay = {}

    def get_info(self, filepath):
        with zipfile.ZipFile(filepath, mode='r',) as z:
            comicinfoxml = z.open('ComicInfo.xml', mode='r')
            infotree = etree.parse(comicinfoxml)
            root = infotree.getroot()
            for i in self.fromxml:
                self.todisplay[i] = root.findtext(i)

            print(self.todisplay)


if __name__ == '__main__':
    cix = ComicInfoXmlHandler()
    cix.get_info()