"""
The class Lang is a language (translation).

Provides an interface to use the languages on the folder "langs"

Use the function get_lang(language_code) to get the language you need and
use the method Lange.get_text(text_code) to get it's language.
"""
import json

_initialized_langs = {}
_available_langs = ["ES-es", "EN-en"]
_lang_synonyms = {"es": "ES-es", "en": "EN-en"}  # Sometimes a language can be named with a synonym.


class Lang:

    def __init__(self, lang_code="EN-en"):

        if lang_code is _lang_synonyms:
            lang_code = _lang_synonyms[lang_code]
        elif lang_code is not _available_langs:
            lang_code = "EN-en"

        with open("langs/%s.json" % lang_code, encoding="utf-8") as f:
            self.texts = json.load(f)

    def get_text(self, text_code, *args, **kwargs):

        if text_code in self.texts:
            try:
                return self.texts[text_code].format(*args, **kwargs)
            except IndexError or KeyError:
                return self.texts[text_code]
        else:
            return self.texts["not_found"].format(failed_text_code=text_code)

    @staticmethod
    def join_text(text_list, separator=" "):
        if not text_list:
            return ""

        result = text_list[0]
        for t in text_list[1:]:
            result = result + separator + t

        return result


def get_lang(lang_code):
    if lang_code in _initialized_langs:
        return _initialized_langs[lang_code]
    else:
        lang = Lang(lang_code)
        _initialized_langs.update({lang_code: lang})
        return lang
