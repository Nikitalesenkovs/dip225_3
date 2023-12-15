import PyPDF2
import pathlib

file=input()
result=0
temp = []
# this part read information from pdf file and place 
# split pdf file in to two pages and extraxt page content to text variables

adrese = pathlib.Path(file)
if not adrese.is_file():
    print(0)
    exit()

if file!="":        
    row=[]
    pdf_file=PyPDF2.PdfReader(open(str(adrese),"rb"))
    page1=pdf_file.pages[0]
    page2=pdf_file.pages[1]
    text1=page1.extract_text()
    text2=page2.extract_text()
    
    pos1 = text1.find("Apmaksai:")
    pos2 = text1.find("Elektroenerģijas patēriņš")
    summa = text1[pos1+10:pos2].replace(",", ".").rstrip()

    pos1 = text2.find("Apjoms Mērv. Cena,")
    per = text2[pos1-7:pos1].rstrip()

    pos1 = text2.find("kWh")
    cena = float(text2[pos1+4:pos1+10].replace(",", ".").rstrip())

    pos1 = text2.find("Apjoms Mērv. Cena,")
    pos2 = text2.find("kWh")
    pater = float(text2[pos1+57:pos2].replace(" ", "").replace(",", ".").rstrip())   #pos1 + 63


 # this part
    with open("nordpool.csv","r") as f:
        next(f)
        for line in f:
            rows = line.rstrip().split(",")
            if rows[0][0:4] == per[3:7] and rows[0][5:7] == per[0:2]: #and (int(row[0][8:9]) >= int(per[0:1]) and int(row[0][8:9]) <= int(per[13:14])):
                temp.append(float(rows[2]))


cena2 = sum(temp)/len(temp)
cena2 = round(cena2,3)

f = cena * pater
s = cena2 * pater
result = f-s
if result > 0:
    result = round(result,1)
    print(result)
else: print(0)
