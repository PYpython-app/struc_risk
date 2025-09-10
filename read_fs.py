import pdfplumber
from ticker import swstocks as stocks
from option import *
import yfinance as yf
import datetime
import numpy as np
struc_fs='CH1372396262_de.pdf'
with pdfplumber.open(struc_fs) as pdf:
    first_page = pdf.pages[0]
    linetxt=first_page.extract_text_simple()
    nbrline=linetxt.count('\n')
    counter=0
    underl=list()
    strike=list()
    barrier=list()
    underlmp=list()
    for x in range(nbrline):
        contentline=(linetxt.split('\n')[x])
        splitline=contentline.split()
        if len(splitline)>9 and len(splitline)<13: # line of interest with needed information
            for y in range(len(splitline)):
                # find the stock
                for bloomtk,tk in stocks.items():
                    if tk == splitline[y]:
                        underl.append(splitline[0])
                        strike.append(splitline[4])
                        barrier.append(splitline[6])
                        underlmpf = yf.Ticker(bloomtk)
                        underlmp.append(underlmpf.info['regularMarketPrice'])
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
print(underl[0],strike[0],barrier[0],underlmp[0])
print(underl[1],strike[1],barrier[1],underlmp[1])
print(underl[2],strike[2],barrier[2],underlmp[2])
print(underl[3],strike[3],barrier[3],underlmp[3])

# I asked Grok and he came up with a good solution for options :-)
today=datetime.date.today()
enddate=datetime.date(int(str_p_year),int(str_p_month),int(str_p_day))
diff=enddate-today
nbrdays=diff.days
yearfrac=nbrdays/365
S0 = np.array([float(underlmp[0]), float(underlmp[1]), float(underlmp[2]), float(underlmp[3])])
barriers=np.array([float(barrier[0]),float(barrier[1]),float(barrier[2]),float(barrier[3])])
r=0.05
sigmas=np.array([0.2,0.2,0.2,0.2])
corr = [
    [1.0, 0.5, 0.5, 0.5],
    [0.5, 1.0, 0.5, 0.5],
    [0.5, 0.5, 1.0, 0.5],
    [0.5, 0.5, 0.5, 1.0]
]
T=yearfrac
N_paths=100000
price, deltas = price_reverse_convertible_multi(S0, barriers, r, sigmas, corr, T, N_paths, compute_delta=True)
print(f"Prix estimé : {price:.2f}")
print(f"Deltas : {deltas}")