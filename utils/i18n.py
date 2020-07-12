from plate import Plate

plate = Plate()


def translate(key, lang, mention=""):
    return plate(key, lang, mention=mention)
