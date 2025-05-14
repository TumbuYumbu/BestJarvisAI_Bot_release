# ai_client.py - файл для доступа к AI-клиентам
import os
import logging
import vertexai
import google.generativeai as genai
from google.api_core.exceptions import FailedPrecondition
from vertexai.language_models import TextGenerationModel, ChatModel
from config import PROJECT_ID, SA_KEY_PATH, GEMINI_API_KEY

logger = logging.getLogger(__name__)

# заготовки для моделей
model = None
classification_model = None
genai_model = None
genai_class_model = None

# === Настройка Vertex AI Gemini (платный) ===
try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
    vertexai.init(project=PROJECT_ID, location="asia-southeast1")
    model = TextGenerationModel.from_pretrained("gemini-1.5-flash")
    classification_model = ChatModel.from_pretrained("gemini-1.5-flash")
except Exception as e:
    logger.error(f"[ai_client] Ошибка инициализации Vertex AI: {e}")

# === Настройка GenAI (бесплатный)  ===
try:
    genai.configure(api_key=GEMINI_API_KEY)
    genai_model = genai.GenerativeModel("gemini-1.5-flash")
    genai_class_model = genai.GenerativeModel("gemini-1.5-flash")
    logger.info("[ai_client] GenAI инициализирована")
except Exception as e:
    logger.error(f"[ai_client] Ошибка инициализации GenAI: {e}")


def text_completion(prompt: str) -> str:
    # сначала пробуем вызвать БЕСплатный GenAI
    if genai_model:
        try:
            return genai_model.generate_content(prompt).text
        except FailedPrecondition as e:
            logger.warning(f"[ai_client] GenAI location error, falling back to Vertex if available: {e}")
            # попытка вызова платного Vertex AI
            if model:
                return model.predict(prompt).text
            # если и платный недоступен — прокидываем ошибку дальше
            raise RuntimeError("Нет доступной текстовой модели Gemini!")

    # Если GenAI не настроен, пробуем Vertex
    if model:
        return model.predict(prompt).text
    raise RuntimeError("Нет доступной текстовой модели Gemini!")



def chat_completion(system_prompt: str, user_prompt: str) -> str:
    # сначала пробуем вызвать БЕСплатный GenAI
    if genai_class_model:
        try:
            combined = system_prompt + "\n\n" + user_prompt
            return genai_class_model.generate_content(combined).text
        except FailedPrecondition as e:
            logger.warning(f"[ai_client] GenAI chat location error: {e}")
            # попытка вызова платногоVertex AI
            if classification_model:
                chat = classification_model.start_chat()
                chat.append_system_message(system_prompt)
                chat.append_user_message(user_prompt)
                return chat.send_message().text
            raise RuntimeError("Нет доступного чат-классификатора Gemini!")

    # Если GenAI-чат не настроен, пробуем платный Vertex-чат
    if classification_model:
            chat = classification_model.start_chat()
            chat.append_system_message(system_prompt)
            chat.append_user_message(user_prompt)
            return chat.send_message().text
    raise RuntimeError("Нет доступного чат-классификатора Gemini!")

