import pdfplumber
import re

class StructuredProduct:
    def __init__(self, name):
        self.name = name
    def get_search_params():
        raise NotImplementedError("Sous-classe doit implémenter get_search_params")

class SP1100(StructuredProduct):
    def __init__(self, underlying, coupon, maturity):
        super().__init__("SP1100")
        self.underlying = underlying
        self.coupon = coupon
        self.maturity = maturity
    def get_search_params():
        return ["coupon", "maturity", "underlying"]

class SP1230(StructuredProduct):
    def __init__(self, underlyings, coupon, maturity, barriers, strike):
        super().__init__("SP1230")
        self.underlyings = underlyings
        self.coupon = coupon
        self.maturity = maturity
        self.barriers = barriers
        self.strike = strike
    def get_search_params():
        return ["coupon", "barriers", "strike", "maturity"]

def extract_params(product, text):
    params = {}
    search_params = product.get_search_params()
    patterns = {
        "coupon": r"coupon\s*(\d+\.?\d*)\s*%",
        "maturity": r"maturity|verfall|rückzahlungstag\s+(\d{2}\.\s*[A-Za-z]+\s+\d{4})",
        "underlying": r"underlying|auf\s+([A-Za-z\s]+)",
        "barriers": r"barrier\s+level\s*\(?(\d+\.?\d*)\s*\%\)?",
        "strike": r"strike\s+level\s*\(?(\d+\.?\d*)\s*\%\)?",
    }
    for param in search_params:
        if param in patterns:
            match = re.search(patterns[param], text, re.IGNORECASE)
            if match:
                value = match.group(1)  # Premier groupe capturé
                if param == "barriers":
                    params[param] = [float(value)]  # Liste pour multi-barrières (à étendre)
                elif param in ["coupon", "strike"]:
                    params[param] = float(value)
                elif param == "maturity":
                    params[param] = value
                elif param == "underlying":
                    params[param] = value.strip()
    return params

#idea : the title of termsheet has all the important info - problem: sometimes on multiple line
filepath=('CH1372396262_de.pdf')
with pdfplumber.open(filepath) as pdf:
    first_page = pdf.pages[0].extract_text()
    first_10_lines = '\n'.join(first_page.split('\n')[:10])
    sspa_match = re.search(r'\b(1[0-9]{3}|2[0-9]{3})\b', first_10_lines)
    sspacode=sspa_match.group() #SSPA code gives type of structured product

# Tester l'extraction
params1230 = extract_params(product1230, text)
params1100 = extract_params(product1100, text)

print("Paramètres pour SP1230 :", params1230)
print("Paramètres pour SP1100 :", params1100)

# Mettre à jour les objets avec les paramètres extraits
for key, value in params1100.items():
    if hasattr(product1100, key):
        setattr(product1100, key, value)
for key, value in params1230.items():
    if hasattr(product1230, key):
        setattr(product1230, key, value if key != "barriers" else [value])
