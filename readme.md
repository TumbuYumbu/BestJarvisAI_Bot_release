# BestJarvisAI

**BestJarvisAI** — это Telegram-бот, работающий на базе Google Gemini (Vertex AI и Generative AI), предназначенный для анализа сообщений пользователей, извлечения личных финансовых операций и сохранения их в Google Sheets. Также бот поддерживает графики, экспорт в Excel и поиск по интернету.

---

## ✨ Возможности

* Автоматическая классификация расходов, доходов и инвестиций из сообщений
* Сохранение данных в Google Sheets с возможностью экспорта в Excel
* Обработка естественного языка через Gemini AI (Vertex AI и GenAI)
* Поддержка цепочек поиска (SEARCH:) через DuckDuckGo
* Создание диаграмм расходов и доходов
* Работа с несколькими пользователями Telegram

---

## 🔧 Установка

1. **Установите Python 3.10+**

2. **Создайте виртуальное окружение (по желанию):**

```bash
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

Содержимое `requirements.txt`:

```
python-telegram-bot==20.0
google-generativeai
google-cloud-vertex-ai
gspread
oauth2client
pandas
matplotlib
duckduckgo-search
python-dotenv>=1.0.0
```

---

## 🔐 Настройка

1. **Создайте `.env`-файл**:

```
CONFIG_JSON_PATH=config.json
```

2. **Создайте `config.json` рядом с `.env` и добавьте в него:**

```json
{
  "PVY_GEMINI_API_KEY": "ваш_ключ_GenAI",
  "BESTJARVISAI_BOT_TELEGRAM_BOT_TOKEN": "токен_бота",
  "GOOGLE_CREDENTIALS_PATH": "путь_к_google_ключу.json",
  "FINANCIAL_BOT_PROJECT_ID": "your-gcp-project-id",
  "GOOGLE_VORTEXAI_APPLICATION_CREDENTIALS": "путь_к_vertexai_ключу.json",
  "SHEET_NAME": "FinanceData",
  "LOG_DIR": "logs"
}
```

---

## ▶️ Запуск

```bash
python main.py
```

Бот начнёт слушать сообщения в Telegram и реагировать на команды.

---

## 🔄 Структура проекта

```
BestJarvisAI/
├── main.py                    # Точка входа
├── BestJarvisAI_Bot.py       # Основная логика Telegram-бота
├── ai_client.py              # Работа с Gemini (Vertex AI и GenAI)
├── google_sheet_client.py    # Работа с Google Sheets
├── config.py                 # Конфигурация проекта
├── config.json               # Настройки и ключи (вне Git)
├── .env                      # Указывает путь к config.json
└── requirements.txt          # Зависимости
```

---

## ⚖️ Команды бота

* `/start` — приветственное сообщение
* `/help` — краткая помощь
* `/reset` — очистка истории общения
* `/chart` — круговая диаграмма доходов/расходов
* `/search <запрос>` — прямой интернет-поиск
* `/export` — выгрузка данных в Excel

Бот также реагирует на обычные текстовые сообщения, классифицирует финансовые операции и предлагает сохранить их.

---

## 🔧 Примечание

* Для использования Vertex AI потребуется GCP-проект и файл сервисного аккаунта
* Для работы с Google Sheets нужно включить Google Drive API и создать ключ доступа
* API Gemini может требовать разных регионов (например, `asia-southeast1`)
