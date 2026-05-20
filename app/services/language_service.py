# app/services/language_service.py

from langdetect import detect


class LanguageService:

    def detect_language(self, text):

        try:

            # Detect Ethiopic characters directly
            if any('\u1200' <= char <= '\u137F' for char in text):
                return "am"

            language = detect(text)

            if language == "am":
                return "am"

            return "en"

        except:
            return "en"