import re   
import pdfplumber
with pdfplumber.open('CH1372396262_de.pdf') as pdf:
    page= pdf.pages[0]
    table_n = page.extract_table()
#print(table_n)
print(len(table_n))
for line in table_n:
    # line is a list
    for field in line:
        if field!=None:
            val1=field.find('SIXSwiss'+'')
            print(field[val1:])
