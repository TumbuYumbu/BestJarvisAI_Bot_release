#google_sheet_client.py - файл для сохранения личных данных в Excel
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

# открывает или создаём лист
# Если errors = False — возвращает / создаёт лист user_{user_id}.
# Если errors = True  — возвращает / создаёт лист "ошибки".
def get_or_create_sheet_for_user(user_id: int, errors: bool = False):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        config.GOOGLE_CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(config.SHEET_NAME)
    title = "ошибки" if errors else f"user_{user_id}"
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows="1000", cols="10")
        if errors:
            ws.append_row(["User ID", "Username", "Дата и время", "Оригинал", "Сырые данные"])
    return ws

def write_valid_data(user_id: int, username: str, rows: list[list[str]]):
    # записывает готовые строки rows в лист пользователя
    ws = get_or_create_sheet_for_user(user_id, errors=False)
    ws.append_rows(rows)

def log_error(user_id: int, username: str, original_msg: str, items: list[dict]):
    # записывает в лист "ошибки" нераспознанное сообщение + сырые items
    ws = get_or_create_sheet_for_user(user_id, errors=True)
    ws.append_row([
        str(user_id),
        f"@{username}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        original_msg,
        json.dumps(items, ensure_ascii=False)
    ])

# вставляет заголовки, если их нет или они не совпадают
def _ensure_headers(ws):
    expected = ["User ID", "Username", "Дата и время",
                "Категория", "Сумма", "Валюта", "Источник"]
    row1 = ws.row_values(1)
    if row1 != expected:
        ws.insert_row(expected, index=1)



# Сохраняет распознанные операции в таблицу
def save_to_google_sheet(user_id: int, username: str, items: list[dict]) -> None:
    ws = get_or_create_sheet_for_user(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for it in items:
        rows.append([
            str(user_id),
            f"@{username}",
            now,
            it["category"].lower(),
            it["amount"],
            normalize_currency(it["currency"]),
            it.get("text", "")
        ])
    if rows:
        ws.append_rows(rows)

# Логирует нераспознанные операции в отдельный лист "ошибки"
def save_failed_to_error_log(user_id: int, username: str,
                             original_msg: str, raw_items: list):
    ws = get_or_create_sheet_for_user("ошибки")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([
        str(user_id), f"@{username}", now,
        original_msg, json.dumps(raw_items, ensure_ascii=False)
    ])
