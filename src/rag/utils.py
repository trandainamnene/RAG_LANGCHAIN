from deep_translator import GoogleTranslator
def translate(text , _from = "en" , _to="vi") :
    translator = GoogleTranslator(source=_from, target=_to)
    rs = translator.translate(text)
    return rs

