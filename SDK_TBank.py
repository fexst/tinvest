import logging
from dataclasses import asdict
from tinkoff.invest import Client, RequestError
from tinkoff.invest.services import InstrumentsService
import configparser

config = configparser.ConfigParser()
config.read("setting.ini")

TOKEN = config['TOKEN']['TOKEN_TINVEST']

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_info_for_instrument(ticker):
    try:
        with Client(TOKEN) as client:
            instruments: InstrumentsService = client.instruments
            tickers = []

            for method in ["shares", "bonds", "etfs", "currencies", "futures"]:
                for item in getattr(instruments, method)().instruments:
                    if item.ticker == ticker or item.uid == ticker:
                        tickers.append(
                            {
                                "name": item.name,
                                "ticker": item.ticker,
                                "figi": item.figi,
                                "lot": item.lot,
                                "currency": item.currency,
                                "uid": item.uid,
                                "type": method
                            }
                        )

        return tickers

    except RequestError as err:
        tracking_id = err.metadata.tracking_id if err.metadata else ""
        error_message = f"Ошибка в get_info_for_instrument\nTracking ID: {tracking_id}\nКод ошибки: {err.code}"
        logger.error(error_message)


def find_last_price(uid):
    try:
        with Client(TOKEN) as client:
            last_price = client.market_data.get_last_prices(instrument_id=[uid])
            price_data = [asdict(price) for price in last_price.last_prices]
            for price_info in price_data:
                raw_time = price_info['time']
                readable_time = raw_time.strftime("%Y-%m-%d %H:%M:%S %Z")
                price_info['time'] = readable_time
            result = price_data[0]

            price = f"{result.get('price').get('units')}.{result.get('price').get('nano')}"
            date_and_time = result.get('time')
            price_and_date = {"price": price, "date_and_time": date_and_time}

            return price_and_date

    except RequestError as err:
        tracking_id = err.metadata.tracking_id if err.metadata else ""
        error_message = f"Ошибка в get_info_for_instrument\nTracking ID: {tracking_id}\nКод ошибки: {err.code}"
        logger.error(error_message)
