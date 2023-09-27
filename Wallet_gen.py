"""Stworzyć generator przykładowych portfeli na wejściu będzie a:ilość inwestycji, b: wartość zainwestowana w zł"""
import random
from pprint import pprint

available_crypto = (
    "ADA",
    "BCH",
    "BTC",
    "DOGE",
    "ETH",
    "LRC",
    "LTC",
    "XRP",
)
price_crypto = {
    "BTC": 113538.0921,
    "ETH": 7116.6315,
    "LTC": 280.4859,
    "ADA": 1.1007,
    "XRP": 2.1927,
    "DOGE": 0.2707,
    "BCH": 898.0016,
    "LRC": 0.7793,
}
dolar = 4.11
invest_values = [10000, 15000, 30000]

# amount_of_crypto=[x for i in range(3):x:=(random.randint(0,len(available_crypto)))]
amount_of_crypto = list(
    map(
        lambda _: random.randint(1, len(available_crypto) - 1),
        range(len(invest_values)),
    )
)
# a = random.sample(range(1, len(available_crypto) - 1), len(amount_of_crypto))

# print(a)


def count_value(p_pln: float, crypto: str):
    price_usd = (p_pln / dolar).__round__(4)
    amount = (p_pln / price_crypto[crypto]).__round__(6)
    return price_usd, amount


def generate_wallet(amount_crytpo: int, invest_value: float):
    """Wygenerać {amount_crytpo} liczb o sumie {invest_value} by stworzyć portfel"""
    crypto_list = list(random.sample(available_crypto, amount_crytpo))
    invest_list = []
    control_sum = 0
    for i in range(len(crypto_list)):
        if i == len(crypto_list) - 1:
            price_pln = invest_value - control_sum
            price_amount = count_value(price_pln, crypto_list[i])
            invest_list.append(
                [crypto_list[i], price_pln, price_amount[0], price_amount[1]]
            )
            break
        if i == 0:
            price_pln = random.randint(1, invest_value * 0.5)
            price_amount = count_value(price_pln, crypto_list[i])

        else:
            price_pln = random.randint(1, (invest_value - control_sum))
            price_amount = count_value(price_pln, crypto_list[i])

        invest_list.append(
            [crypto_list[i], price_pln, price_amount[0], price_amount[1]]
        )
        control_sum += price_pln

    return invest_list


"""result: name, price_pln, price_USD,amount"""
for i in range(len(invest_values)):
    wallet = generate_wallet(amount_of_crypto[i], invest_values[i])
    for j in range(len(wallet)):
        wallet[j] = ",".join([str(i) for i in wallet[j]])

    with open(f"Wallets_gene\\wallet_gen_{i}.csv", "w") as file:
        file.write("\n".join(wallet))
