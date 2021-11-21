"""Constants to use in Nomics integration."""
DOMAIN = "nomics"
ATTRIBUTION = "Crypto Market Cap & Pricing Data Provided By Nomics"
DEFAULT_ICON = "mdi:cash-multiple"
DEFAULT_NAME = "Nomics Sensor"
SCAN_INTERVAL_MINUTES = 1
SPECIAL_ICONS = {
    "BTC": "mdi:currency-btc",
    "ETH": "mdi:currency-eth",
    "EUR": "mdi:currency-eur",
    "USD": "mdi:currency-usd",
}
MANUFACTURER = "Nomics"

ATTR_NAME = "name"
ATTR_LOGO_URL = "logo_url"
ATTR_STATUS = "status"
ATTR_PRICE_TIMESTAMP = "price_timestamp"
ATTR_RANK = "rank"

ATTRIBUTES = [ATTR_NAME, ATTR_LOGO_URL, ATTR_STATUS, ATTR_PRICE_TIMESTAMP, ATTR_RANK]

ATTR_HIST_1D = "1d"
ATTR_HIST_7D = "7d"

HIST_ATTRIBUTES = [ATTR_HIST_1D, ATTR_HIST_7D]
