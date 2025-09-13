import pdfplumber
import re
filepath=('CH1361311306_de_20240722_150408.pdf')
with pdfplumber.open(filepath) as pdf:
    nbrpage=len(pdf.pages)
    pattern = re.compile(r'Anfangskurs|Referenzkurs|Barriere')
    intpg={}
    for x in range(nbrpage):
        pagetxt=pdf.pages[x].extract_text()
        matches = pattern.finditer(pagetxt)
        matchcnt=0
        for match in matches:
            # Find the interesting page i.e. the page with the most matche
            matchcnt+=1
        intpg[x]=matchcnt
    bestpage=max(intpg,key=intpg.get)
    print(bestpage)



