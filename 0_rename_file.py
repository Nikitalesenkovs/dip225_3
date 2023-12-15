# Importē nepieciešamās bibliotēkas
import PyPDF2
import pathlib

# Ievada faila nosaukumu
file = input()
result = 0
temp = []

# Pārbauda, vai fails pastāv
adrese = pathlib.Path(file)
if not adrese.is_file():
    print(0)
    exit()

# Pārbauda, vai ievadītais faila nosaukums nav tukšs
if file != "":
    # Atver PDF failu un iegūst lapas
    pdf_file = PyPDF2.PdfReader(open(str(adrese), "rb"))
    page1 = pdf_file.pages[0]
    page2 = pdf_file.pages[1]
    text1 = page1.extract_text()
    text2 = page2.extract_text()

    # Atrodi informāciju par maksājumu
    pos1 = text1.find("Apmaksai:")
    pos2 = text1.find("Elektroenerģijas patēriņš")
    summa = text1[pos1 + 10:pos2].replace(",", ".").rstrip()

    # Atrodi informāciju par elektroenerģijas patēriņu un cenu
    pos1 = text2.find("Apjoms Mērv. Cena,")
    per = text2[pos1 - 7:pos1].rstrip()
    pos1 = text2.find("kWh")
    cena = float(text2[pos1 + 4:pos1 + 10].replace(",", ".").rstrip())
    pos1 = text2.find("Apjoms Mērv. Cena,")
    pos2 = text2.find("kWh")
    pater = float(text2[pos1 + 57:pos2].replace(" ", "").replace(",", ".").rstrip())   # pos1 + 63

    # Iegūst datus no "nordpool.csv" un pievieno temp sarakstam
    with open("nordpool.csv", "r") as f:
        next(f)
        for line in f:
            rows = line.rstrip().split(",")
            if rows[0][0:4] == per[3:7] and rows[0][5:7] == per[0:2]:
                temp.append(float(rows[2]))

# Aprēķina jauno cenu, pamatojoties uz "nordpool.csv"
cena2 = sum(temp) / len(temp)
cena2 = round(cena2, 3)

# Aprēķina summu un izvada rezultātu
f = cena * pater
s = cena2 * pater
result = f - s
if result > 0:
    result = round(result, 1)
    print(result)
else:
    print(0)
