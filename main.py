import yfinance as finance


def formatPeriods(ticker):
    original = '................................................'
    length = len(ticker)
    total = 3 - length
    if total == 0:
        return original
    elif total < 0:
        return original.removesuffix('.' * abs(total))
    else:
        return original + (abs(total) * '.')


def dividendDiscountModel(quarterlyDividend, dividendGrowthPerYear):
    calc1 = (quarterlyDividend * 4) * (1 + dividendGrowthPerYear)
    return calc1


def gordonGrowthModel(quarterlyDividend, dividendGrowthPerYear, equityCapitalCost):
    calc1 = dividendDiscountModel(quarterlyDividend, dividendGrowthPerYear)
    calc2 = calc1 / (equityCapitalCost - dividendGrowthPerYear)
    return calc2


def valLowerThanZero(calc):
    if calc < 0:
        return float(0.00)
    else:
        return calc


def percentLowerThanZero(GGM, marketPrice):
    calc = round((((GGM - marketPrice) / marketPrice) * 100), 2)
    if calc < 0:
        return 'N/A\n\n\t\t\t\t\033[1;31;49mCAUTION: Overvalued stock, do not buy!'
    else:
        return str(calc) + '%\n\n\t\t\t\t\033[1;32;49mStock is undervalued, this is a good time to buy!'


ticker = input('What is the ticker of your stock?\t').upper()
retrieveData = finance.Ticker(ticker).info
marketPrice = retrieveData['regularMarketPrice']

quarterlyDividend = float(input('What is the quarterly dividend of this stock (in USD)?\t'))

dividendGrowthPerYear = float(input('What is the expected dividend growth rate per year (as a percentage)?\t')) / 100

equityCapitalCost = float(input('What is the company\'s cost of equity capital (as a percentage)?\t')) / 100

DDM = dividendDiscountModel(quarterlyDividend, dividendGrowthPerYear)
GGM = gordonGrowthModel(quarterlyDividend, dividendGrowthPerYear, equityCapitalCost)

print('\nCurrent valuation of ' + str(ticker) + ' ' + formatPeriods(ticker) + ' $' + str(marketPrice))

print('Valuation based on the DDM and GGM ...................................... $' + str(round(valLowerThanZero(GGM), 2)))

print('Difference between current valuation and calculated valuation ........... '
      + str(percentLowerThanZero(GGM, marketPrice)))