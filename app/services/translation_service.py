from app.translations.messages import MESSAGES


class TranslationService:

    def translate(self, language: str, key: str):

        return (
            MESSAGES.get(language, MESSAGES["en"])
            .get(key, key)
        )