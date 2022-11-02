import requests
from tok import currency


class BotException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(cur1, cur2, volume):
        try:
            cur1_name = currency[cur1.upper()]
        except KeyError:
            raise BotException(f"Валюта {cur1} не найдена!")

        try:
            cur2_name = currency[cur2.upper()]
        except KeyError:
            raise BotException(f"Валюта {cur2} не найдена!")

        if cur1 == cur2:
            raise BotException(f'Выбрана одна и таже валюта - {cur1.upper()} ({currency[cur1.upper()]}) !')

        try:
            volume = float(volume.replace(",", "."))
        except ValueError:
            raise BotException(f'Количество введено неверно {volume}!')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/f3c35ba640bef029ad7b804f/pair/{cur1}/{cur2}").json()
        exch = r["conversion_rate"] * volume
        exch = round(exch, 2)
        answer = f"Стоимость {volume} {cur1.upper()} ({cur1_name}) равна {exch} {cur2.upper()} ({cur2_name})"
        return answer
