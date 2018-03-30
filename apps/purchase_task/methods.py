
'''This method will return an array of price levels as strings
    formatted to look like dollars with two decimals (e.g., $2.00 '''

def get_price_as_dollar_string(price_levels):
    price_as_dollar = []
    for level in price_levels:
        price_as_dollar.append("${:.2f}".format((float(level) / 100)))
    return price_as_dollar
# return an array of prices formatted as strings

def get_price_as_float(price_levels):
    price_level = []
    for level in price_levels:
        price_level.append(float(level) / 100)
    return price_level
# return an array of prices formatted as strings

def get_price_dictionary(PRICES):
    price_strings = get_price_as_dollar_string(PRICES)
    prices_as_float = get_price_as_float(PRICES)
    price_dictionary = {}
    for i in range(len(price_strings)):
        price_dictionary["{}".format(i)] = PRICES[i]
    return price_dictionary
