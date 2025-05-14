# config.py - файл с конфигурированием бота
import os
import json
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv

# в ключаем логгинг
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# грузим переменные конфигурации
load_dotenv()                   	
CONFIG_JSON_PATH = os.environ.get("CONFIG_JSON_PATH", "config.json")

try:
	with open(CONFIG_JSON_PATH, "r", encoding="utf-8-sig") as f:
   	 _cfg = json.load(f)

	# API keys & tokens
	GEMINI_API_KEY          = _cfg["PVY_GEMINI_API_KEY"]
	TELEGRAM_BOT_TOKEN      = _cfg["BESTJARVISAI_BOT_TELEGRAM_BOT_TOKEN"]

	# Google Sheets
	GOOGLE_CREDENTIALS_PATH = _cfg["GOOGLE_CREDENTIALS_PATH"]
	SHEET_NAME              = _cfg.get("SHEET_NAME", "FinanceData")

	# Vertex AI
	PROJECT_ID              = _cfg["FINANCIAL_BOT_PROJECT_ID"]
	SA_KEY_PATH             = _cfg["GOOGLE_VORTEXAI_APPLICATION_CREDENTIALS"]

	# Logging dir
	LOG_DIR = Path(_cfg.get("LOG_DIR", "logs"))
	LOG_DIR.mkdir(parents=True, exist_ok=True)

except Exception as e:
    logger.error(f"Не удалось загрузить конфиг из {CONFIG_JSON_PATH}: {e}")
    sys.exit(1)

# категории личных финансов
CATEGORY_EXPENSE    = "расход"
CATEGORY_INCOME     = "доход"
CATEGORY_INVESTMENT = "инвестиции"
CATEGORY_OTHER      = "другое"
ALLOWED_CATEGORIES  = {
    CATEGORY_EXPENSE,
    CATEGORY_INCOME,
    CATEGORY_INVESTMENT,
    CATEGORY_OTHER
}

# перекодировка допустимых валют
CURRENCY_RUB = "RUB"
CURRENCY_USD = "USD"
CURRENCY_EUR = "EUR"
CURRENCY_CNY = "CNY"
CURRENCY_MAP = {
    "₽": CURRENCY_RUB, "руб.": CURRENCY_RUB, "руб": CURRENCY_RUB, "рублей": CURRENCY_RUB, "рубля": CURRENCY_RUB,
    "$": CURRENCY_USD, "доллар": CURRENCY_USD, "долларов": CURRENCY_USD, "usd": CURRENCY_USD,
    "€": CURRENCY_EUR, "евро": CURRENCY_EUR,
    "юань": CURRENCY_CNY, "юаней": CURRENCY_CNY, "юаня": CURRENCY_CNY, "¥": CURRENCY_CNY
}

# глубина вложенного автопоиска в интернете
MAX_SEARCH_DEPTH = 5
