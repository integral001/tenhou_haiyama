import gzip
import xml.etree.ElementTree as ET

def read_mjlog(path):
    """return xml_root from filepath"""
    try:
        tree = ET.parse(path)
    except:
        #unzip for old version
        try:
            mjlog = gzip.open(path)
            tree = ET.parse(mjlog)
        except:
            raise
    root = tree.getroot()
    return root

def get_shuffle_ver(xml_mjlog):
    shuffle = xml_mjlog.find("SHUFFLE")
    if shuffle is None:
        return "mt19937ar"
    seed = shuffle.attrib["seed"].split(",")
    shuffle_ver = seed[0]
    return shuffle_ver

def get_seed(xml_mjlog):
    seed = []
    shuffle_ver = get_shuffle_ver(xml_mjlog)
    if shuffle_ver == "mt19937ar":
        inits = xml_mjlog.findall("INIT")
        for init in inits:
            shuffle_attr = init.attrib["shuffle"].split(",")
            init_seed = [int(elem, 16) for elem in shuffle_attr[1:]]
            seed.append(init_seed)
        pass
    elif shuffle_ver in ["mt19937ar-sha512-n288", "mt19937ar-sha512-n288-base64"]:
        shuffle = xml_mjlog.find("SHUFFLE")
        seed_attr = shuffle.attrib["seed"].split(",")
        if shuffle_ver in ["mt19937ar-sha512-n288"]:
            seed = [int(elem, 16) for elem in seed_attr[1:]]
        else:
            seed = seed_attr[1:][0]
    return seed

def count_round(xml_mjlog):
    inits = xml_mjlog.findall("INIT")
    num_kyoku = len(inits)
    return num_kyoku

if __name__ == '__main__':
    paths = [
        "mjlog/2008092000gm-0009-0000-10db094d&tw=0.mjlog",
        "mjlog/2009090100gm-00a9-0000-6920f1ac&tw=3.mjlog",
        "mjlog/2016022509gm-0009-0000-b327da61.mjlog",
    ]

    shuffle_ver = []
    seed = []
    num_round = []
    for path in paths:
        xml = read_mjlog(path)
        shuffle_ver.append(get_shuffle_ver(xml))
        seed.append(get_seed(xml))
        num_round.append(count_round(xml))

    print("done")
