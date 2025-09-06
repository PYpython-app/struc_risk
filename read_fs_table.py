import re
import pdfplumber
# extract the title line of product
with pdfplumber.open('CH1367331019_de.pdf') as pdf:
    page= pdf.pages[0]
    table_n =page.extract_text()
    table=table_n.split('\n')
    # the title line is always on the beginning of TS
    for i in range(7):
        find_pct=re.findall('%',table[i])
        if len(find_pct)>0:
            most_imp_line = table[i]
            # now we need to extract the key input and store them
            # most_imp_line is a string !
            def_struc=most_imp_line.split()
            print (len(def_struc))
            coupon=(def_struc)[0]
            print (coupon)
            type_struc=def_struc[2]+def_struc[3]+def_struc[4]+def_struc[5]
            print (type_struc)
            und1_struc=def_struc[7]
            und2_struc=def_struc[8]
            und3_struc=def_struc[9]
            #und4_struc=def_struc[10]
