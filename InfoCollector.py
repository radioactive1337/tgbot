from requests import Session

from bot_data import cmc_api_key


class InfoCollector:
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f'{cmc_api_key}',
    }

    @staticmethod
    def market_gatherer(h=headers):
        url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
        session = Session()
        session.headers.update(h)
        req = session.get(url)
        data = req.json()
        total_market_cap = float(data.get("data").get("quote").get("USD").get("total_market_cap"))
        total_volume_24h = float(data.get("data").get("quote").get("USD").get("total_volume_24h"))
        total_mcap_percentage_change = float(
            data.get("data").get("quote").get("USD").get("total_market_cap_yesterday_percentage_change"))
        btc_dominance = float(data.get("data").get("btc_dominance"))
        return (f"market cap   -->   {'{0:,}'.format(round(total_market_cap)).replace(',', ' ')}\n"
                f"24h volume   -->   {'{0:,}'.format(round(total_volume_24h)).replace(',', ' ')}\n"
                f"mcap change %   -->   {'{0:,}'.format(round(total_mcap_percentage_change, 3)).replace(',', ' ')}\n"
                f"btc dominance   -->   {'{0:,}'.format(round(btc_dominance, 3)).replace(',', ' ')}")

    @staticmethod
    def coin_info_gatherer(h=headers, symbol="btc"):
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        par = {
            "symbol": f"{symbol}"
        }
        session = Session()
        session.headers.update(h)
        req = session.get(url, params=par)
        data = req.json()
        symbol = data.get("data").get(f"{symbol}")[0].get("symbol")
        price = float(data.get("data").get(f"{symbol}")[0].get("quote").get("USD").get("price"))
        percent_change_30d = float(
            data.get("data").get(f"{symbol}")[0].get("quote").get("USD").get("percent_change_30d"))
        market_cap = float(data.get("data").get(f"{symbol}")[0].get("quote").get("USD").get("market_cap"))
        market_cap_dominance = float(
            data.get("data").get(f"{symbol}")[0].get("quote").get("USD").get("market_cap_dominance"))
        return (f"{symbol}\n"
                f"price   -->   {round(price, 3)}\n"
                f"30d change %   -->   {round(percent_change_30d, 3)}\n"
                f"mcap   -->   {'{0:,}'.format(round(market_cap)).replace(',', ' ')}\n"
                f"dominance   -->   {round(market_cap_dominance, 3)}")