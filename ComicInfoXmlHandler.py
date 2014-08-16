import zipfile
import xml.etree.ElementTree as etree
import io



class ComicInfoXmlHandler():

    def __init__(self, fromxml, filepath):
        self.fromxml = fromxml

        with zipfile.ZipFile(filepath, mode='r',) as z:
            comicinfoxml = z.open('ComicInfo.xml', mode='r')
            self.infotree = etree.parse(comicinfoxml)
            self.root = self.infotree.getroot()

    def get_info(self):
        todisplay = {}
        for i in self.fromxml:
            todisplay[i] = self.root.findtext(i)
        return todisplay

    def generate_xml(self, toxml):
        g = io.StringIO()
        for i in toxml:
            if (toxml[i] != '') & (self.root.find(i) is not None):
                self.root.find(i).text = toxml[i]
            elif (toxml[i] != '') & (self.root.find(i) is None):
                newelem = etree.Element(i)
                newelem.text = toxml[i]
                self.root.find('ComicInfo').append(newelem)
            elif toxml[i] == '':
                self.root.find(i).remove
        self.infotree.write(g, encoding='unicode')
        return g

    def write_info(self, xml2write, filepath):
        with zipfile.ZipFile(filepath, mode='w',) as z:
            z.writestr('ComicInfo.xml', xml2write.getvalue())


if __name__ == '__main__':
    cix = ComicInfoXmlHandler()
    cix.get_info()