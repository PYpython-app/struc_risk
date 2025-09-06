import pdfplumber
Stocks=['ABBNSW',
        'ALCSW',
        'GEBNSW',
        'AMRZSW',
        'GIVNSW',
        'HOLNSW',
        'KNINSW',
        'LOGNSW',
        'LONNSW',
        'NESNSW',
        'NOVNSW',
        'PGHNSW',
        'CFRSW',
        'ROGSW'
        'SIKASW',
        'SOONSW',
        'SLHNSW',
        'SRENSW',
        'SCMNSW',
        'UBSGSW',
        'ZURNSW']

struc_fs=('CH1372396262_de.pdf')
with pdfplumber.open(struc_fs) as pdf:
    first_page = pdf.pages[0]
    linetxt=first_page.extract_text_simple()
    nbrline=linetxt.count('\n')
    counter=0
    underl=list()
    strike=list()
    barrier=list()
    for x in range(nbrline):
        contentline=(linetxt.split('\n')[x])
        splitline=contentline.split()
        if len(splitline)>9 and len(splitline)<13:
            for y in range(len(splitline)):
                if splitline[y] in Stocks:
                    underl.append(splitline[0])
                    strike.append(splitline[4])
                    barrier.append(splitline[6])
                    counter+=1

#les paramètres de l'option sont ok, il manque la maturité...
expiry=['Verfall','DatedeConstatationFinale']
optexpiry=list()
with pdfplumber.open(struc_fs) as pdf:
    first_page = pdf.pages[1]
    linetxt=first_page.extract_text_simple()
    nbrline=linetxt.count('\n')
    for x in range(nbrline):
        contentline=(linetxt.split('\n')[x])
        splitline=contentline.split()
        for y in range(len(splitline)):
            if splitline[y] in expiry:
                optexpiry.append(splitline[1])
# decompose expiry date in dd mm yyyy
strg_date=optexpiry[0]
str_p_end=strg_date[:10]
str_p_day=strg_date[:2]
str_p_month=strg_date[3:5]
str_p_year=strg_date[6:10]
print(str_p_day,str_p_month,str_p_year)
print(strike)
print(barrier)
print(underl)

# for exotic option : code of tavaresiqueira library installed pip3 install exotic-options
# gross approach one exotic for every component, it is wrong but product is retail :-)
# I asked Grok and he came up with a good solution for options :-)