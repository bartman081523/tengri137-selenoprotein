import json
import numpy as np

# Define Gematria values
gematria_values = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70,
    'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

# Functions for conversions
def text_to_gematria(text):
    return [gematria_values.get(letter, 0) for letter in text if gematria_values.get(letter, 0) != 0]

def gematria_to_text(gematria):
    return "".join(letter for value in gematria for letter, val in gematria_values.items() if val == value)

# Functions for mathematical operations
def calculate_sum_and_product(gematria):
    sum_ = sum(gematria)
    # Use np.prod with dtype=np.float64 to handle large numbers
    product = np.prod(np.array(gematria, dtype=np.float64))
    return sum_, product

def calculate_inverses(sum_, product):
    inverse_sum = 1 / sum_ if sum_ != 0 else 'infinity'
    inverse_product = 1 / product if product != 0 else 'infinity'
    return inverse_sum, inverse_product

# Main logic
results = []
ftorah = open("sefer_yetzirah.json", "r").read()
for chapter in json.loads(ftorah)["text"]:
    for verse in chapter:
        gematria = text_to_gematria(verse.replace(" ", ""))
        if gematria:  # Ensure the list is not empty
            sum_, product = calculate_sum_and_product(gematria)
            inverse_sum, inverse_product = calculate_inverses(sum_, product)
            print(f"Verse: {verse}\nGematria:{gematria}\nSum: {sum_}\nProduct: {product}\nInverse of Sum: {inverse_sum}\nInverse of Product: {inverse_product}\n")
            results.append(gematria)
