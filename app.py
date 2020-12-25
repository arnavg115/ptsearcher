from flask import Flask,redirect,url_for,render_template,request,session
from fuzzywuzzy import process
data = [['No.', 'AtomicWeight', 'Name', 'Sym.', 'M.P.(°C)', '\xa0B.P.\xa0(°C)', 'Density*(g/cm3)', 'Earthcrust (%)*', 'Discovery(Year)', 'Group*', 'Electronconfiguration', 'Ionizationenergy (eV)'], ['1', '1.008', 'Hydrogen', 'H', '-259', '-253', '0.09', '0.14', '1776', '1', '1s1', '13.60'], ['2', '4.003', 'Helium', 'He', '-272', '-269', '0.18', '', '1895', '18', '1s2', '24.59'], ['3', '6.941', 'Lithium', 'Li', '180', '1,347', '0.53', '', '1817', '1', '[He] 2s1', '5.39'], ['4', '9.012', 'Beryllium', 'Be', '1,278', '2,970', '1.85', '', '1797', '2', '[He] 2s2', '9.32'], ['5', '10.811', 'Boron', 'B', '2,300', '2,550', '2.34', '', '1808', '13', '[He] 2s2 2p1', '8.30'], ['6', '12.011', 'Carbon', 'C', '3,500', '4,827', '2.26', '0.09', 'ancient', '14', '[He] 2s2 2p2', '11.26'], ['7', '14.007', 'Nitrogen', 'N', '-210', '-196', '1.25', '', '1772', '15', '[He] 2s2 2p3', '14.53'], ['8', '15.999', 'Oxygen', 'O', '-218', '-183', '1.43', '46.71', '1774', '16', '[He] 2s2 2p4', '13.62'], ['9', '18.998', 'Fluorine', 'F', '-220', '-188', '1.70', '0.03', '1886', '17', '[He] 2s2 2p5', '17.42'], ['10', '20.180', 'Neon', 'Ne', '-249', '-246', '0.90', '', '1898', '18', '[He] 2s2 2p6', '21.56'], ['11', '22.990', 'Sodium', 'Na', '98', '883', '0.97', '2.75', '1807', '1', '[Ne] 3s1', '5.14'], ['12', '24.305', 'Magnesium', 'Mg', '639', '1,090', '1.74', '2.08', '1755', '2', '[Ne] 3s2', '7.65'], ['13', '26.982', 'Aluminum', 'Al', '660', '2,467', '2.70', '8.07', '1825', '13', '[Ne] 3s2 3p1', '5.99'], ['14', '28.086', 'Silicon', 'Si', '1,410', '2,355', '2.33', '27.69', '1824', '14', '[Ne] 3s2 3p2', '8.15'], ['15', '30.974', 'Phosphorus', 'P', '44', '280', '1.82', '0.13', '1669', '15', '[Ne] 3s2 3p3', '10.49'], ['16', '32.065', 'Sulfur', 'S', '113', '445', '2.07', '0.05', 'ancient', '16', '[Ne] 3s2 3p4', '10.36'], ['17', '35.453', 'Chlorine', 'Cl', '-101', '-35', '3.21', '0.05', '1774', '17', '[Ne] 3s2 3p5', '12.97'], ['18', '39.948', 'Argon', 'Ar', '-189', '-186', '1.78', '', '1894', '18', '[Ne] 3s2 3p6', '15.76'], ['19', '39.098', 'Potassium', 'K', '64', '774', '0.86', '2.58', '1807', '1', '[Ar] 4s1', '4.34'], ['20', '40.078', 'Calcium', 'Ca', '839', '1,484', '1.55', '3.65', '1808', '2', '[Ar] 4s2', '6.11'], ['21', '44.956', 'Scandium', 'Sc', '1,539', '2,832', '2.99', '', '1879', '3', '[Ar] 3d1 4s2', '6.56'], ['22', '47.867', 'Titanium', 'Ti', '1,660', '3,287', '4.54', '0.62', '1791', '4', '[Ar] 3d2 4s2', '6.83'], ['23', '50.942', 'Vanadium', 'V', '1,890', '3,380', '6.11', '', '1830', '5', '[Ar] 3d3 4s2', '6.75'], ['24', '51.996', 'Chromium', 'Cr', '1,857', '2,672', '7.19', '0.04', '1797', '6', '[Ar] 3d5 4s1', '6.77'], ['25', '54.938', 'Manganese', 'Mn', '1,245', '1,962', '7.43', '0.09', '1774', '7', '[Ar] 3d5 4s2', '7.43'], ['26', '55.845', 'Iron', 'Fe', '1,535', '2,750', '7.87', '5.05', 'ancient', '8', '[Ar] 3d6 4s2', '7.90'], ['27', '58.933', 'Cobalt', 'Co', '1,495', '2,870', '8.90', '', '1735', '9', '[Ar] 3d7 4s2', '7.88'], ['28', '58.693', 'Nickel', 'Ni', '1,453', '2,732', '8.90', '0.02', '1751', '10', '[Ar] 3d8 4s2', '7.64'], ['29', '63.546', 'Copper', 'Cu', '1,083', '2,567', '8.96', '', 'ancient', '11', '[Ar] 3d10 4s1', '7.73'], ['30', '65.390', 'Zinc', 'Zn', '420', '907', '7.13', '', 'ancient', '12', '[Ar] 3d10 4s2', '9.39'], ['31', '69.723', 'Gallium', 'Ga', '30', '2,403', '5.91', '', '1875', '13', '[Ar] 3d10 4s2 4p1', '6.00'], ['32', '72.640', 'Germanium', 'Ge', '937', '2,830', '5.32', '', '1886', '14', '[Ar] 3d10 4s2 4p2', '7.90'], ['33', '74.922', 'Arsenic', 'As', '81', '613', '5.72', '', 'ancient', '15', '[Ar] 3d10 4s2 4p3', '9.79'], ['34', '78.960', 'Selenium', 'Se', '217', '685', '4.79', '', '1817', '16', '[Ar] 3d10 4s2 4p4', '9.75'], ['35', '79.904', 'Bromine', 'Br', '-7', '59', '3.12', '', '1826', '17', '[Ar] 3d10 4s2 4p5', '11.81'], ['36', '83.800', 'Krypton', 'Kr', '-157', '-153', '3.75', '', '1898', '18', '[Ar] 3d10 4s2 4p6', '14.00'], ['37', '85.468', 'Rubidium', 'Rb', '39', '688', '1.63', '', '1861', '1', '[Kr] 5s1', '4.18'], ['38', '87.620', 'Strontium', 'Sr', '769', '1,384', '2.54', '', '1790', '2', '[Kr] 5s2', '5.69'], ['39', '88.906', 'Yttrium', 'Y', '1,523', '3,337', '4.47', '', '1794', '3', '[Kr] 4d1 5s2', '6.22'], ['40', '91.224', 'Zirconium', 'Zr', '1,852', '4,377', '6.51', '0.03', '1789', '4', '[Kr] 4d2 5s2', '6.63'], ['41', '92.906', 'Niobium', 'Nb', '2,468', '4,927', '8.57', '', '1801', '5', '[Kr] 4d4 5s1', '6.76'], ['42', '95.940', 'Molybdenum', 'Mo', '2,617', '4,612', '10.22', '', '1781', '6', '[Kr] 4d5 5s1', '7.09'], ['43', '98.000', 'Technetium', 'Tc', '2,200', '4,877', '11.50', '', '1937', '7', '[Kr] 4d5 5s2', '7.28'], ['44', '101.070', 'Ruthenium', 'Ru', '2,250', '3,900', '12.37', '', '1844', '8', '[Kr] 4d7 5s1', '7.36'], ['45', '102.906', 'Rhodium', 'Rh', '1,966', '3,727', '12.41', '', '1803', '9', '[Kr] 4d8 5s1', '7.46'], ['46', '106.420', 'Palladium', 'Pd', '1,552', '2,927', '12.02', '', '1803', '10', '[Kr] 4d10', '8.34'], ['47', '107.868', 'Silver', 'Ag', '962', '2,212', '10.50', '', 'ancient', '11', '[Kr] 4d10 5s1', '7.58'], ['48', '112.411', 'Cadmium', 'Cd', '321', '765', '8.65', '', '1817', '12', '[Kr] 4d10 5s2', '8.99'], ['49', '114.818', 'Indium', 'In', '157', '2,000', '7.31', '', '1863', '13', '[Kr] 4d10 5s2 5p1', '5.79'], ['50', '118.710', 'Tin', 'Sn', '232', '2,270', '7.31', '', 'ancient', '14', '[Kr] 4d10 5s2 5p2', '7.34'], ['51', '121.760', 'Antimony', 'Sb', '630', '1,750', '6.68', '', 'ancient', '15', '[Kr] 4d10 5s2 5p3', '8.61'], ['52', '127.600', 'Tellurium', 'Te', '449', '990', '6.24', '', '1783', '16', '[Kr] 4d10 5s2 5p4', '9.01'], ['53', '126.905', 'Iodine', 'I', '114', '184', '4.93', '', '1811', '17', '[Kr] 4d10 5s2 5p5', '10.45'], ['54', '131.293', 'Xenon', 'Xe', '-112', '-108', '5.90', '', '1898', '18', '[Kr] 4d10 5s2 5p6', '12.13'], ['55', '132.906', 'Cesium', 'Cs', '29', '678', '1.87', '', '1860', '1', '[Xe] 6s1', '3.89'], ['56', '137.327', 'Barium', 'Ba', '725', '1,140', '3.59', '0.05', '1808', '2', '[Xe] 6s2', '5.21'], ['57', '138.906', 'Lanthanum', 'La', '920', '3,469', '6.15', '', '1839', '3', '[Xe] 5d1 6s2', '5.58'], ['58', '140.116', 'Cerium', 'Ce', '795', '3,257', '6.77', '', '1803', '101', '[Xe] 4f1 5d1 6s2', '5.54'], ['59', '140.908', 'Praseodymium', 'Pr', '935', '3,127', '6.77', '', '1885', '101', '[Xe] 4f3 6s2', '5.47'], ['60', '144.240', 'Neodymium', 'Nd', '1,010', '3,127', '7.01', '', '1885', '101', '[Xe] 4f4 6s2', '5.53'], ['61', '145.000', 'Promethium', 'Pm', '1,100', '3,000', '7.30', '', '1945', '101', '[Xe] 4f5 6s2', '5.58'], ['62', '150.360', 'Samarium', 'Sm', '1,072', '1,900', '7.52', '', '1879', '101', '[Xe] 4f6 6s2', '5.64'], ['63', '151.964', 'Europium', 'Eu', '822', '1,597', '5.24', '', '1901', '101', '[Xe] 4f7 6s2', '5.67'], ['64', '157.250', 'Gadolinium', 'Gd', '1,311', '3,233', '7.90', '', '1880', '101', '[Xe] 4f7 5d1 6s2', '6.15'], ['65', '158.925', 'Terbium', 'Tb', '1,360', '3,041', '8.23', '', '1843', '101', '[Xe] 4f9 6s2', '5.86'], ['66', '162.500', 'Dysprosium', 'Dy', '1,412', '2,562', '8.55', '', '1886', '101', '[Xe] 4f10 6s2', '5.94'], ['67', '164.930', 'Holmium', 'Ho', '1,470', '2,720', '8.80', '', '1867', '101', '[Xe] 4f11 6s2', '6.02'], ['68', '167.259', 'Erbium', 'Er', '1,522', '2,510', '9.07', '', '1842', '101', '[Xe] 4f12 6s2', '6.11'], ['69', '168.934', 'Thulium', 'Tm', '1,545', '1,727', '9.32', '', '1879', '101', '[Xe] 4f13 6s2', '6.18'], ['70', '173.040', 'Ytterbium', 'Yb', '824', '1,466', '6.90', '', '1878', '101', '[Xe] 4f14 6s2', '6.25'], ['71', '174.967', 'Lutetium', 'Lu', '1,656', '3,315', '9.84', '', '1907', '101', '[Xe] 4f14 5d1 6s2', '5.43'], ['72', '178.490', 'Hafnium', 'Hf', '2,150', '5,400', '13.31', '', '1923', '4', '[Xe] 4f14 5d2 6s2', '6.83'], ['73', '180.948', 'Tantalum', 'Ta', '2,996', '5,425', '16.65', '', '1802', '5', '[Xe] 4f14 5d3 6s2', '7.55'], ['74', '183.840', 'Tungsten', 'W', '3,410', '5,660', '19.35', '', '1783', '6', '[Xe] 4f14 5d4 6s2', '7.86'], ['75', '186.207', 'Rhenium', 'Re', '3,180', '5,627', '21.04', '', '1925', '7', '[Xe] 4f14 5d5 6s2', '7.83'], ['76', '190.230', 'Osmium', 'Os', '3,045', '5,027', '22.60', '', '1803', '8', '[Xe] 4f14 5d6 6s2', '8.44'], ['77', '192.217', 'Iridium', 'Ir', '2,410', '4,527', '22.40', '', '1803', '9', '[Xe] 4f14 5d7 6s2', '8.97'], ['78', '195.078', 'Platinum', 'Pt', '1,772', '3,827', '21.45', '', '1735', '10', '[Xe] 4f14 5d9 6s1', '8.96'], ['79', '196.967', 'Gold', 'Au', '1,064', '2,807', '19.32', '', 'ancient', '11', '[Xe] 4f14 5d10 6s1', '9.23'], ['80', '200.590', 'Mercury', 'Hg', '-39', '357', '13.55', '', 'ancient', '12', '[Xe] 4f14 5d10 6s2', '10.44'], ['81', '204.383', 'Thallium', 'Tl', '303', '1,457', '11.85', '', '1861', '13', '[Xe] 4f14 5d10 6s2 6p1', '6.11'], ['82', '207.200', 'Lead', 'Pb', '327', '1,740', '11.35', '', 'ancient', '14', '[Xe] 4f14 5d10 6s2 6p2', '7.42'], ['83', '208.980', 'Bismuth', 'Bi', '271', '1,560', '9.75', '', 'ancient', '15', '[Xe] 4f14 5d10 6s2 6p3', '7.29'], ['84', '209.000', 'Polonium', 'Po', '254', '962', '9.30', '', '1898', '16', '[Xe] 4f14 5d10 6s2 6p4', '8.42'], ['85', '210.000', 'Astatine', 'At', '302', '337', '0.00', '', '1940', '17', '[Xe] 4f14 5d10 6s2 6p5', '9.30'], ['86', '222.000', 'Radon', 'Rn', '-71', '-62', '9.73', '', '1900', '18', '[Xe] 4f14 5d10 6s2 6p6', '10.75'], ['87', '223.000', 'Francium', 'Fr', '27', '677', '0.00', '', '1939', '1', '[Rn] 7s1', '4.07'], ['88', '226.000', 'Radium', 'Ra', '700', '1,737', '5.50', '', '1898', '2', '[Rn] 7s2', '5.28'], ['89', '227.000', 'Actinium', 'Ac', '1,050', '3,200', '10.07', '', '1899', '3', '[Rn] 6d1 7s2', '5.17'], ['90', '232.038', 'Thorium', 'Th', '1,750', '4,790', '11.72', '', '1829', '102', '[Rn] 6d2 7s2', '6.31'], ['91', '231.036', 'Protactinium', 'Pa', '1,568', '0', '15.40', '', '1913', '102', '[Rn] 5f2 6d1 7s2', '5.89'], ['92', '238.029', 'Uranium', 'U', '1,132', '3,818', '18.95', '', '1789', '102', '[Rn] 5f3 6d1 7s2', '6.19'], ['93', '237.000', 'Neptunium', 'Np', '640', '3,902', '20.20', '', '1940', '102', '[Rn] 5f4 6d1 7s2', '6.27'], ['94', '244.000', 'Plutonium', 'Pu', '640', '3,235', '19.84', '', '1940', '102', '[Rn] 5f6 7s2', '6.03'], ['95', '243.000', 'Americium', 'Am', '994', '2,607', '13.67', '', '1944', '102', '[Rn] 5f7 7s2', '5.97'], ['96', '247.000', 'Curium', 'Cm', '1,340', '0', '13.50', '', '1944', '102', '', '5.99'], ['97', '247.000', 'Berkelium', 'Bk', '986', '0', '14.78', '', '1949', '102', '', '6.20'], ['98', '251.000', 'Californium', 'Cf', '900', '0', '15.10', '', '1950', '102', '', '6.28'], ['99', '252.000', 'Einsteinium', 'Es', '860', '0', '0.00', '', '1952', '102', '', '6.42'], ['100', '257.000', 'Fermium', 'Fm', '1,527', '0', '0.00', '', '1952', '102', '', '6.50'], ['101', '258.000', 'Mendelevium', 'Md', '0', '0', '0.00', '', '1955', '102', '', '6.58'], ['102', '259.000', 'Nobelium', 'No', '827', '0', '0.00', '', '1958', '102', '', '6.65'], ['103', '262.000', 'Lawrencium', 'Lr', '1,627', '0', '0.00', '', '1961', '102', '', '4.90'], ['104', '261.000', 'Rutherfordium', 'Rf', '0', '0', '0.00', '', '1964', '4', '', '0.00'], ['105', '262.000', 'Dubnium', 'Db', '0', '0', '0.00', '', '1967', '5', '', '0.00'], ['106', '266.000', 'Seaborgium', 'Sg', '0', '0', '0.00', '', '1974', '6', '', '0.00'], ['107', '264.000', 'Bohrium', 'Bh', '0', '0', '0.00', '', '1981', '7', '', '0.00'], ['108', '277.000', 'Hassium', 'Hs', '0', '0', '0.00', '', '1984', '8', '', '0.00'], ['109', '268.000', 'Meitnerium', 'Mt', '0', '0', '0.00', '', '1982', '9', '', '0.00']]
with open("a.txt","r") as txt:
    read = txt.read().split("\n")
with open("c.txt","r") as txt1:
    reader= txt1.read().split("\n")
def matcher(query, choices, limit=1):
    return process.extract(query, choices,limit = limit)
m = "m"
app = Flask(__name__)
app.secret_key = "Iamsmartveryverysmart"
@app.route("/")
def slash():
    return redirect(url_for("home"))
@app.route("/home")
def home():
    return render_template("main.html")
@app.route("/sources")
def sources():
    return render_template("sources.html")
@app.route("/formatting")
def formatting():
    return render_template("formating.html")
@app.route("/srchpage",methods = ["GET","POST"])
def srchpage():
    if request.method == "POST":
        num = request.form["number"]
        session["num"]=num
        return redirect(url_for("results"))
    else:
        f = 0
        return render_template("srchpage.html",h = f)
@app.route("/error")
def error():
    return render_template("error.html")
@app.route("/pricing")
def pricing():
    return render_template("pricing.html")
@app.route("/results",methods = ["GET", "POST"])
def results():
    if "num" in session:
        num = session["num"]
        j=[]
        if request.method == "POST":
            if int(num) == 1:
                aasdu = request.form["d1"]
                n=[]
                try:
                    int(aasdu)
                except ValueError:
                    if len(aasdu)>2:
                        aasdu = matcher(aasdu, read)
                    else:
                         aasdu = matcher(aasdu,reader)
                    aasdu = aasdu[0]
                    (name, matchscore) = aasdu
                    aasdu = name
                for row in data:
                        for field in row:
                            if field == aasdu:
                                n.append(row)
                                row = n[0]
                                dict = {
                                    "numm":row[0],
                                    "weight":row[1],
                                    "namee":row[2],
                                    "sym":row[3],
                                    "mp":row[4]+"°C",
                                    "bp":row[5]+"°C",
                                    "disc":row[8],
                                    "group":row[9],
                                    "elconfig":row[10]
                                    }
                return render_template("moresearch.html",h= int(num),dict = dict,n=1)
            elif int(num) ==2:
                n=[]
                aasdu = request.form["d1"]
                natl = request.form["d2"]
                try:
                    int(aasdu)
                except ValueError:
                    if len(aasdu)>2:
                        aasdu = matcher(aasdu, read)
                    else:
                         aasdu = matcher(aasdu,reader)
                    n=[]
                    aasdu = aasdu[0]
                    (name, matchscore) = aasdu
                    aasdu = name
                for row in data:
                    for field in row:
                        if field == aasdu:
                            n.append(row)
                            row = n[0]
                            dict1 = {
                                "numm":row[0],
                                "weight":row[1],
                                "namee":row[2],
                                "sym":row[3],
                                "mp":row[4]+"°C",
                                "bp":row[5]+"°C",
                                "disc":row[8],
                                "group":row[9],
                                "elconfig":row[10]
                                }
                n1=[]
                try:
                    int(natl)
                except ValueError:
                    if len(natl)>2:
                        natl = matcher(natl, read)
                    else:
                         natl= matcher(natl,reader)
                    n=[]
                    natl= natl[0]
                    (name, matchscore) = natl
                    natl = name
                for row1 in data:
                    for field1 in row1:
                        if field1 == natl:
                            n1.append(row1)
                            row1= n1[0]
                            dict2 = {
                                "numm":row1[0],
                                "weight":row1[1],
                                "namee":row1[2],
                                "sym":row1[3],
                                "mp":row1[4]+"°C",
                                "bp":row1[5]+"°C",
                                "disc":row1[8],
                                "group":row1[9],
                                "elconfig":row1[10]
                                }
                return render_template("moresearch.html",h= int(num),dict = dict1,n=2,dict2 = dict2)
            elif int(num) ==3:
                j.append(request.form["d1"])
                j.append(request.form["d2"])
                j.append(request.form["d3"])
                n=[]
                aasdu = j[0]
                try:
                    int(aasdu)
                except ValueError:
                    if len(aasdu)>2:
                        aasdu = matcher(aasdu, read)
                    else:
                         aasdu = matcher(aasdu,reader)
                    n=[]
                    aasdu = aasdu[0]
                    (name, matchscore) = aasdu
                    aasdu = name
                for row in data:
                    for field in row:
                        if field == aasdu:
                            n.append(row)
                            row = n[0]
                            dict1 = {
                                "numm":row[0],
                                "weight":row[1],
                                "namee":row[2],
                                "sym":row[3],
                                "mp":row[4]+"°C",
                                "bp":row[5]+"°C",
                                "disc":row[8],
                                "group":row[9],
                                "elconfig":row[10]
                                }
                natl=j[1]
                n1=[]
                try:
                    int(natl)
                except ValueError:
                    if len(natl)>2:
                        natl = matcher(natl, read)
                    else:
                         natl= matcher(natl,reader)
                    n=[]
                    natl= natl[0]
                    (name, matchscore) = natl
                    natl = name
                for row1 in data:
                    for field1 in row1:
                        if field1 == natl:
                            n1.append(row1)
                            row1= n1[0]
                            dict2 = {
                                "numm":row1[0],
                                "weight":row1[1],
                                "namee":row1[2],
                                "sym":row1[3],
                                "mp":row1[4]+"°C",
                                "bp":row1[5]+"°C",
                                "disc":row1[8],
                                "group":row1[9],
                                "elconfig":row1[10]
                                }
                naty = j[2]
                n2=[]
                try:
                    int(naty)
                except ValueError:
                    if len(naty)>2:
                        naty = matcher(naty, read)
                    else:
                         naty = matcher(naty,reader)
                    
                    naty = naty[0]
                    (name, matchscore) = naty
                    naty = name
                for row2 in data:
                    for field2 in row2:
                        if field2 == naty:
                            n2.append(row2)
                            row2= n2[0]
                            dict3 = {
                                "numm":row2[0],
                                "weight":row2[1],
                                "namee":row2[2],
                                "sym":row2[3],
                                "mp":row2[4]+"°C",
                                "bp":row2[5]+"°C",
                                "disc":row2[8],
                                "group":row2[9],
                                "elconfig":row2[10]
                                }
                return render_template("moresearch.html",h= int(num),dict = dict1,n=3,dict2 = dict2,dict3 = dict3)
        else:
            return render_template("moresearch.html",h= int(num),n=0)
    else:
        return "false"
if __name__ == "__main__":
    app.run(debug = True)