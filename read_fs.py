import pdfplumber
from ticker import swstocks as stocks
from option import *
import yfinance as yf
import datetime
import numpy as np
from tkinter import *
from tkinter import filedialog

# Global variables
filepath = None
underl = []
strike = []
barrier = []
underlmp = []
optexpiry = []
# Function to choose the file and when chosen the computation starts
def open_file():
    global filepath, underl, strike, barrier, underlmp, optexpiry
    filepath = filedialog.askopenfilename(filetypes=[("Structured Product Termsheet File", "*.pdf")])
    if not filepath:
        messagebox.showwarning("Warning", "No file selected")
        return

    # Reinitialize list
    underl.clear()
    strike.clear()
    barrier.clear()
    underlmp.clear()
    optexpiry.clear()
    with pdfplumber.open(filepath) as pdf:
            first_page = pdf.pages[0]
            linetxt = first_page.extract_text_simple()
            nbrline = linetxt.count('\n')
            counter = 0
            for x in range(nbrline):
                contentline = (linetxt.split('\n')[x])
                splitline = contentline.split()
                if len(splitline) > 9 and len(splitline) < 13:  # line of interest with needed information
                    for y in range(len(splitline)):
                        # find the stock
                        for bloomtk, tk in stocks.items():
                            if tk == splitline[y]:
                                underl.append(splitline[0])
                                strike.append(splitline[4])
                                barrier.append(splitline[6])
                                underlmpf = yf.Ticker(bloomtk)
                                underlmp.append(underlmpf.info['regularMarketPrice'])
                                counter += 1
        # les paramètres de l'option sont ok, il manque la maturité...
            expiry = ['Verfall', 'DatedeConstatationFinale']
            optexpiry = list()
            with pdfplumber.open(filepath) as pdf:
                first_page = pdf.pages[1]
                linetxt = first_page.extract_text_simple()
                nbrline = linetxt.count('\n')
                for x in range(nbrline):
                    contentline = (linetxt.split('\n')[x])
                    splitline = contentline.split()
                    for y in range(len(splitline)):
                        if splitline[y] in expiry:
                            optexpiry.append(splitline[1])
            # decompose expiry date in dd mm yyyy
            strg_date = optexpiry[0]
            str_p_end = strg_date[:10]
            str_p_day = strg_date[:2]
            str_p_month = strg_date[3:5]
            str_p_year = strg_date[6:10]

            # I asked Grok and he came up with a good solution for options :-)
            today = datetime.date.today()
            enddate = datetime.date(int(str_p_year), int(str_p_month), int(str_p_day))
            diff = enddate - today
            nbrdays = diff.days
            yearfrac = nbrdays / 365
            n = len(underlmp)
            S0 = np.array([float(underlmp[i]) for i in range(n)])
            barriers = np.array([float(barrier[i]) for i in range(n)])
            r = 0.05
            sigmas = np.array([0.2]*n)
            corr = [[0.5 if i != j else 1.0 for j in range(n)] for i in range(n)]
            T = yearfrac
            N_paths = 100000
            price, deltas = price_reverse_convertible_multi(S0, barriers, r, sigmas, corr, T, N_paths, compute_delta=True)
# New window with result
            result_window = Toplevel(window)
            result_window.title("Analysis results")
            result_window.geometry("800x600")
            result_window.config(background="lightgray")

            Label(result_window, text="Results", font=('arial', 20, 'bold'), bg="lightgray").pack(pady=10)
            Label(result_window, text=f"Estimated price : {price:.2f}", font=('arial', 15), bg="lightgray").pack(pady=5)
            Label(result_window, text=f"Deltas : {deltas}", font=('arial', 15), bg="lightgray").pack(pady=5)
            for i in range(n):
                Label(result_window, text=f"{underl[i]} - Strike: {strike[i]}, Barrier: {barrier[i]}, Price: {underlmp[i]:.2f}",
                      font=('arial', 12), bg="lightgray").pack(pady=2)
            # Close result window
            Button(result_window, text="Close", command=result_window.destroy, font=('arial', 12)).pack(pady=10)
# GUI avec Tkinter
window=Tk()
window.geometry("1600x800")
window.title("Structured Product Analysis")
window.config(background = "black")
label_txt=Label(window,
            text='Stuctured Product Analysis',
            font=('arial',70,'bold'),
            fg='black',
            bg='#008aa6',
            relief=RAISED,
            bd=10)
label_txt.place(x=350,y=10)
label_instr=Label(window,
            text='To run the analysis you must select a file first and then press run the analysis',
            font=('arial',30,'bold'),
            fg='black',
            bg='white',
            relief=RAISED,
            bd=10)
label_instr.place(x=300,y=250)
label_warning=Label(window,
            text='WARNING! The termsheets files must be in the same directory as the program',
            font=('arial',50,'bold'),
            fg='red',
            bg='white',
            relief=RAISED,
            bd=10,
            wraplength=1500)
label_warning.place(x=20,y=650)
but_openf=Button(window, text='1. Click to select termsheet')
but_openf.config(font=('arial',25,'bold'))
but_openf.config(command=open_file)
but_openf.place(x=300, y=400)
but_run=Button(window, text='2. Run the analysis')
but_run.config(font=('arial',25,'bold'))
but_run.place(x=300, y=500)
window.mainloop()