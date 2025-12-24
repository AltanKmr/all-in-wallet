import re
from datetime import datetime, date, timedelta
import calendar
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter

forex = {"USD": "$", "TRY": "₺", "EUR": "€", "GBP": "£", "JPY" : "¥",
         "AUD" : "$(the Australian dollar)", "CAD" : "$(the Canadian dollar)",
         "CNY" : "CN¥", "NZD" : "$(the New Zealand dollar)", "BRL" : "S$(the Brazilian real )" , "HKD" : "HK$(the Hong Kong dollar)"}

crypto ={"BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin", "SOL": "solana",
         "XRP": "ripple", "DOGE": "dogecoin", "ADA": "cardano", "TRX": "tron",
         "LTC": "litecoin", "AVAX": "avalanche-2"}


def luhn(n):
    n = n.replace("-", "")[::-1]
    evens = n[1::2]
    odds = n[::2]

    result = 0
    for x in evens:
        if int(x)*2 < 10:
            result += (int(x)*2)
        else:
            tens = 0
            for a in list(str(int(x)*2)):
                tens += int(a)
            result += tens
    for y in odds:
        result += int(y)

    if result % 10 == 0:
        return True
    else:
        return False

def visa(n):
    if n[0] == "4" and len(n) == 19:
        return True
def mastercard(n):
    if (51 <= int(n[:2]) <= 55 or 2221 <= int(n[:4]) <= 2720) and len(n) == 19:
        return True
def amex(n):
    if (n[:2] == "34" or n[:2] == "37") and len(n) == 17:
        return True
def discover(n):
    if (n[:2] == 65 or n[:4] == "6011" or 644 <= int(n[:3]) <= 649) and len(n) == 19:
        return True
def maestro(n):
    if (n[:2] == "50" or 56 <= int(n[:2]) <= 69) and 14 <= len(n) <= 23:
        return True
def jcb(n):
    if 3528 <= int(n[:4]) <= 3589 and 19 <= len(n) <= 23:
        return True
def main():
    def dict1planner(form):
        for i in range(len(symbols)):
            form += f"{paralar[i]}{symbols[i]}"
            if i != (len(symbols) - 1):
                form += ", "
        ccNdatas[cc][1] = form

    def dict2planner(form):
        for i in range(len(coinler)):
            form += f"{adetler[i]}{coinler[i]}"
            if i != (len(coinler) - 1):
                form += ", "
        ccNdatas[cc][2] = form
    name = input("Please Enter Your Full Name: ").strip().title()
    space = name.count(" ")
    while not name or name.isdecimal == True or space < 1:
        print("Please Enter Valid Name.")
        name = input("Please Enter Your Full Name: ").strip().title()
        space = name.count(" ")

    today = str(datetime.today()).split()

    date = str(today[0]).split("-")
    time = int(today[1][:2])

    year, month, day = int(date[0]), int(date[1]), int(date[2])

    d = calendar.weekday(year, month, day)

    name_d, name_m = list(calendar.day_name)[d], list(calendar.month_name)[month]

    print(f"\n{day} {name_m} {year} {name_d}\n")

    if time >= 22 or time < 6:
        print(f"Good Night, {name}")
    elif time >= 18:
        print(f"Good Evening, {name}")
    elif time >= 12:
        print(f"Good Afternoon, {name}")
    elif time >= 6:
        print(f"Good Morning, {name}")


    while True:
        cc = input("Please Type Credit/Bank Card Number: ").strip()
        if re.search(r"^\d{4}-\d{4}-\d{4}(-\d{1,3})?$|^\d{4}-\d{4}-\d{4}-\d{4}(-\d{1,3})?$|^\d{4}-\d{6}-\d{5}$",cc):
                break
        else:
            print("\nInvalid Formation...")
    if luhn(cc):
        print("It's a valid ", end="")
        if visa(cc): print("VISA"); t = "VISA"
        if mastercard(cc): print("MASTERCARD"); t = "MASTERCARD"
        if amex(cc): print("AMERICAN EXPRESS"); t = "AMERICAN EXPRESS"
        if discover(cc): print("DISCOVER"); t = "DISCOVER"
        if maestro(cc): print("MAESTRO"); t = "MAESTRO"
        if jcb(cc): print("JCB"); t = "JCB"

        cc = cc.replace("-", "")

        titles = ["Credit/Bank Card", "\tPayment Type", "\tCurrencies", "\tCoins", "\tTotal Balance(in USD)", "\tPnL(from last enterance)\n"]

        f = open("wallet.txt", "r+")
        all_lines_f = f.readlines()
        if all_lines_f == []:
            f.writelines(titles)
        formattedL, cardnumbers = [], []
        for i in all_lines_f[1:]:
            i = i.strip().split("\t")
            formattedL.append(i)
        for x in formattedL:
            cardnumbers.append(x[0])

        if not cc in cardnumbers:
            entry = [cc, f"\t{t}", "\t0.0$", "\t0.0BTC", "\t0.0$", f"\t+0.0$({day}/{today[0][5:7]}/{year} {today[1][:5]})\n"]
            for entries in entry:
                f.write(entries)
            f.close()



        buttons = f"\n[1] Deposit the money into your card\n[2] Withdraw the money from your card\n[3] Foreign Exchanges\n[4] Buy/Sell Crypto Currencies\n[5] Log out from your account"
        print(buttons)

        while True:

            new_f = open("wallet.txt", "r+")
            totalines = new_f.readlines()[1:]

            ccNdatas = {}
            for lines in totalines:
                lines = lines.strip().split("\t")
                ccNdatas[lines[0]] = [lines[1],lines[2],lines[3],lines[4],lines[5]]

            f = CurrencyConverter()
            c = CoinGeckoAPI()


            variables = ccNdatas[cc][1].split(", ")

            symbols, paralar = [], []

            for infos in variables:
                pattern = re.match(r"(\d+\.\d+)(.+)", infos)
                if pattern:
                    para = float(pattern.group(1))
                    paralar.append(para)
                    symbol = pattern.group(2)
                    symbols.append(symbol)

            coins = ccNdatas[cc][2].split(", ")

            coinler, adetler = [], []

            for datas in coins:
                model = re.match(r"(\d+\.\d+)(.+)", datas)
                if model:
                    adet = float(model.group(1))
                    adetler.append(adet)
                    coin = model.group(2)
                    coinler.append(coin)

            hint = ""
            abbres = []
            for i in symbols:
                v = list(forex.values()).index(i)
                k = list(forex.keys())[v]
                abbres.append(k)
                hint += f"'{k}' for '{i}', "

            model_balance = ccNdatas[cc][3]
            modelb = re.match(r"(\d+\.\d+)(.)", model_balance)
            if modelb:
                current_balance = float(modelb.group(1))

            total_usd_forex, total_usd_crypto, balance = 0, 0, 0

            option = int(input("\nPress available number and then press enter to transactions: "))
            while not 1 <= option <= 5:
                print(buttons)
                option = int(input("Press available number and then press enter to transactions: "))

            if 1 <= option <= 4:

                if option == 1:
                    print(f"\nCurrent rates for transactions are", end="")
                    for rates in list(forex.keys()):
                        if list(forex.keys()).index(rates) == 10:
                            print(f" and {rates}", end = "")
                        else:
                            print(f" {rates},", end = "")
                    print("\n")

                    currency = input("Which exchange rate will you use to deposit money: ").upper()
                    while currency not in list(forex.keys()):
                        if len(currency) != 3 or currency.isalpha() == False:
                            print("Please type 3-code abbreviation...")
                        else:
                            print("Not available currency...")
                        currency = input("Which exchange rate will you use to deposit money: ").upper()

                    deposit = input(f"How much {currency} do you request to deposit: ")
                    while deposit.isdecimal() == False:
                        print("Enter integers...")
                        deposit = input(f"How much {currency} do you request to deposit: ")
                    deposit = int(deposit)

                    isaret = forex[currency]

                    if isaret in symbols:
                        idx = symbols.index(isaret)
                        x = int(paralar[idx])
                        x += deposit
                        paralar[idx] = format(x, ".1f")
                    else:
                        paralar.append(format(deposit, ".1f"))
                        symbols.append(isaret)
                        abbres.append(currency)

                    formatted_variables = ""
                    dict1planner(formatted_variables)
                    print(buttons)

                if option == 2:

                    print(f"In your account, you have;")

                    for i in range(len(symbols)):
                        print(f"=> {paralar[i]}{symbols[i]}      ", end = "")

                    currency2 = input(f"\nWhich exchange rate will you use to withdraw money (type {hint}): ").upper()
                    while currency2 not in abbres:
                        if len(currency2) != 3 or currency2.isalpha() == False:
                            print("Please type 3-code abbreviation...")
                        else:
                            print("Not available currency...")
                        currency2 = input(f"Which exchange rate will you use to withdraw money (type {hint}): ").upper()

                    user_currency = forex[currency2]
                    yer = symbols.index(user_currency)
                    user_money = float(paralar[yer])

                    if int(user_money) == 0:
                        print(f"Insufficient funds. You have {user_money}{user_currency}. You must increment fund first.")
                    else:
                        withdraw = input(f"How much {currency2} do you request to withdraw: ")
                        while withdraw.isalpha():
                            print("Enter numbers...")
                            withdraw = input(f"How much {currency2} do you request to withdraw: ")

                        while float(withdraw) > user_money:
                            print(f"Insufficient funds. You have {user_money}{user_currency} .")
                            withdraw = input(f"How much {currency2} do you request to withdraw: ")

                        new_user_money = user_money - float(withdraw)
                        paralar[yer] = new_user_money

                        formatted_variables2 = ""
                        dict1planner(formatted_variables2)
                    print(buttons)

                if option == 3:

                    print(f"In your account, you have;")

                    for i in range(len(symbols)):
                        print(f"=> {paralar[i]}{symbols[i]}      ", end = "")

                    currency3 = input(f"\nWhich exchange rate will you use for foreign currencies (type {hint}): ").upper()
                    while currency3 not in abbres:
                        if len(currency3) != 3 or currency3.isalpha() == False:
                            print("Please type 3-code abbreviation...")
                        else:
                            print("Not available currency...")
                        currency3 = input(f"Which exchange rate will you use for foreign currencies (type {hint}): ").upper()

                    user_currency2 = forex[currency3]
                    yer2 = symbols.index(user_currency2)
                    user_money2 = float(paralar[yer2])

                    if int(user_money2) == 0:
                        print(f"Insufficient funds. You have {user_money2}{user_currency2}. You must increment fund first.")
                    else:
                        for_frx = []
                        for i in list(forex.keys()):
                            if i != currency3:
                                for_frx.append(i)
                        parametres = {}
                        for frx in for_frx:
                            x = f.convert(1, frx, currency3)
                            print(f"{frx}{currency3} = {x:.4f}")
                            x = format(x, ".4f")
                            parametres[frx] = float(x)

                        currency4 = input(f"\nWhich exchange rate's parametre will you use for forex: ").upper()
                        while currency4 not in for_frx:
                            if len(currency4) != 3 or currency4.isalpha() == False:
                                print("Please type 3-code abbreviation...")
                            else:
                                print("Not available parametre...")
                            currency4 = input(f"\nWhich exchange rate's parametre will you use for forex: ").upper()




                        amount = input(f"How much {currency4} do you request to exchange (Account => {user_money2}{user_currency2}) ({currency4}{currency3} = {parametres[currency4]}): ")
                        while amount.isalpha():
                            print("Enter numbers...")
                            amount = input(f"How much {currency4} do you request to exchange (Account => {user_money2}{user_currency2}) ({currency4}{currency3} = {parametres[currency4]}): ")

                        amount = int(amount)
                        requirement = amount * float(parametres[currency4])


                        while requirement > user_money2:
                            more = round(requirement - user_money2, 2)
                            print(f"Insufficient fund. You need more than {more}{user_currency2}")
                            amount = input(f"How much {currency4} do you request to exchange (Account => {user_money2}{user_currency2}) ({currency4}{currency3} = {parametres[currency4]}): ")
                            amount = int(amount)
                            requirement = amount * float(parametres[currency4])

                        if forex[currency4] in symbols:
                            idx = symbols.index(forex[currency4])
                            x = float(paralar[idx])
                            x += amount
                            paralar[idx] = format(x, ".2f")
                        else:
                            paralar.append(format(amount, ".2f"))
                            symbols.append(forex[currency4])
                            abbres.append(currency4)

                        new_user_money = format(user_money2 - requirement, ".2f")
                        paralar[yer2] = new_user_money

                        formatted_variables3 = ""
                        dict1planner(formatted_variables3)
                    print(buttons)

                if option == 4:
                    print(f"In your crypto wallet, you have;")

                    for i in range(len(coinler)):
                        print(f"# {adetler[i]}{coinler[i]}      ", end = "")

                    bs = input("Would you like to Buy or Sell cryptocurrency: ").lower()
                    while bs != "buy" and bs != "sell":
                        print("Choose one of the two options...")
                        bs = input("Would you like to Buy or Sell cryptocurrency: ").lower()

                    if bs == "sell":

                        user_coin = input(f"\nWhich cryptocurrency will you use to sell: ").upper()
                        while user_coin not in coinler:
                            if len(user_coin) != 3 or user_coin.isalpha() == False:
                                print("Please type 3-code abbreviation...")
                            else:
                                print("Not available cryptocurrency...")
                            user_coin = input(f"\nWhich cryptocurrency will you use to sell: ").upper()

                        yeri = coinler.index(user_coin)
                        user_coin_value = float(adetler[yeri])

                        if int(user_coin_value) == 0:
                            print(f"Insufficient funds. You have {user_coin_value}{user_coin}. You must increment fund first.")
                        else:
                            parametres2 = {}
                            for frx in forex:
                                x = c.get_price(ids=crypto[user_coin], vs_currencies=frx)
                                print(f"{user_coin}{frx} = {x[crypto[user_coin]][frx.lower()]} ")
                                parametres2[frx] = float(x[crypto[user_coin]][frx.lower()])

                            convert_frx = input(f"\nWhich crypto rate's currency will you purchase: ").upper()
                            while convert_frx not in forex:
                                if len(convert_frx) != 3 or convert_frx.isalpha() == False:
                                    print("Please type 3-code abbreviation...")
                                else:
                                    print("Not available parametre...")
                                convert_frx = input(f"\nWhich crypto rate's currency will you purchase: ").upper()


                            sell_amount = input(f"How much {user_coin} do you request to sell (Crypto wallet => {user_coin_value}{user_coin}) ({user_coin}{convert_frx} = {parametres2[convert_frx]}): ")
                            while sell_amount.isalpha():
                                print("Enter numbers...")
                                sell_amount = input(f"How much {user_coin} do you request to sell (Crypto wallet => {user_coin_value}{user_coin}) ({user_coin}{convert_frx} = {parametres2[convert_frx]}): ")

                            sell_amount = float(sell_amount)

                            while sell_amount > user_coin_value:
                                more = round(sell_amount - user_coin_value, 4)
                                print(f"Insufficient fund. You need more than {more}{user_coin}")
                                sell_amount = input(f"How much {user_coin} do you request to sell (Crypto wallet => {user_coin_value}{user_coin}) ({user_coin}{convert_frx} = {parametres2[convert_frx]}): ")
                                sell_amount = float(sell_amount)

                            taken = sell_amount * parametres2[convert_frx]

                            if forex[convert_frx] in symbols:
                                idx = symbols.index(forex[convert_frx])
                                x = float(paralar[idx])
                                x += taken
                                paralar[idx] = format(x, ".2f")
                            else:
                                paralar.append(format(taken, ".2f"))
                                symbols.append(forex[convert_frx])
                                abbres.append(convert_frx)

                            new_user_coin_value = format(user_coin_value - sell_amount, ".4f")
                            adetler[yeri] = new_user_coin_value

                            formatted_variables4 = ""
                            dict1planner(formatted_variables4)
                            dict2planner(formatted_variables4)
                        print(buttons)
                    if bs == "buy":
                        print(f"In your account, you have;")

                        for i in range(len(symbols)):
                            print(f"=> {paralar[i]}{symbols[i]}      ", end = "")

                        currency5 = input(f"\nWhich exchange rate will you use to purchase cryptocurrencies (type {hint}): ").upper()
                        while currency5 not in abbres:
                            if len(currency5) != 3 or currency5.isalpha() == False:
                                print("Please type 3-code abbreviation...")
                            else:
                                print("Not available currency...")
                            currency5 = input(f"\nWhich exchange rate will you use to purchase cryptocurrencies (type {hint}): ").upper()

                        user_currency3 = forex[currency5]
                        yer3 = symbols.index(user_currency3)
                        user_money3 = float(paralar[yer3])

                        if int(user_money3) == 0:
                            print(f"Insufficient funds. You have {user_money3}{user_currency3}. You must increment fund first.")
                        else:
                            print(f"\nCurrent coins for transactions are", end="")
                            for j in list(crypto.keys()):
                                if list(crypto.keys()).index(j) == 9:
                                    print(f" and {j}", end = "")
                                else:
                                    print(f" {j},", end = "")
                            print("\n")

                            parametres3 = {}
                            for cry in crypto:
                                x = c.get_price(ids=crypto[cry], vs_currencies=currency5)
                                print(f"{cry}{currency5} = {x[crypto[cry]][currency5.lower()]} ")
                                parametres3[cry] = float(x[crypto[cry]][currency5.lower()])

                            buy_coin = input("Which coin will you purchase: ").upper()
                            while buy_coin not in list(crypto.keys()):
                                print("Not available cryptocurrency...")
                                buy_coin = input("Which coin will you purchase: ").upper()

                            spent = input(f"How much {currency5} do you use to buy coins (Account => {user_money3}{user_currency3}) ({currency5}{buy_coin} = {parametres3[buy_coin]}): ")
                            while spent.isalpha():
                                print("Enter numbers...")
                                spent = input(f"How much {currency5} do you use to buy coins (Account => {user_money3}{user_currency3}) ({currency5}{buy_coin} = {parametres3[buy_coin]}): ")

                            spent = float(spent)

                            while spent > user_money3:
                                more = round(spent - user_money3, 4)
                                print(f"Insufficient fund. You need more than {more}{user_money3}")
                                spent = input(f"How much {currency5} do you use to buy coins (Account => {user_money3}{user_currency3}) ({currency5}{buy_coin} = {parametres3[buy_coin]}): ")
                                spent = float(spent)

                            added_coin = spent / parametres3[buy_coin]

                            if buy_coin in coinler:
                                idx = coinler.index(buy_coin)
                                x = float(adetler[idx])
                                x += added_coin
                                adetler[idx] = format(x, ".7f")
                            else:
                                adetler.append(format(added_coin, ".7f"))
                                coinler.append(buy_coin)

                            new_user_money2 = format(user_money3 - spent, ".2f")
                            paralar[yer3] = new_user_money2

                            formatted_variables5 = ""
                            dict1planner(formatted_variables5)
                            dict2planner(formatted_variables5)
                        print(buttons)

                for abbre in abbres:
                    char = forex[abbre]
                    i = symbols.index(char)
                    deger = paralar[i]
                    x = f.convert(deger, abbre, 'USD')
                    total_usd_forex += x

                for coin in coinler:
                    location = coinler.index(coin)
                    adet = adetler[location]
                    x = c.get_price(ids=crypto[coin], vs_currencies='usd')
                    adet = x[crypto[coin]]['usd'] * float(adet)
                    total_usd_crypto += adet

                balance = total_usd_forex + total_usd_crypto
                pol = balance - current_balance
                ccNdatas[cc][3] = f"{format(balance, ".2f")}$"
                if pol > 0:
                    new_pnl = f"+{format(pol,".2f")}$({day}/{today[0][5:7]}/{year} {today[1][:5]})"
                else:
                    new_pnl = f"{format(pol,".2f")}$({day}/{today[0][5:7]}/{year} {today[1][:5]})"

                ccNdatas[cc][4] = new_pnl


                l = []
                len_of_cc = 0
                first_line = ""
                for i in titles:
                    first_line += i
                l.append(first_line)
                for a in ccNdatas:
                    every_line = ""
                    every_line += a
                    for i in range(len(ccNdatas[a])):
                        if i == 4 and len_of_cc != (len(ccNdatas) - 1):
                            xd = f"\t{ccNdatas[a][i]}\n"
                            len_of_cc += 1
                        else:
                            xd = f"\t{ccNdatas[a][i]}"
                        every_line += xd
                    l.append(every_line)

                asd = open("wallet.txt", "w")
                asd.writelines(l)
                asd.close()

            if option == 5:
                print(f"\nYour account has been successfully logged out.\nSee You Later {name}...")
                break
if __name__ == "__main__":
    main()
