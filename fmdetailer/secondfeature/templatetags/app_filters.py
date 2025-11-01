from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    """ Pozwala na dostęp do klucza słownika przez zmienną w szablonie. """
    return dictionary.get(key)

@register.filter
def replace(value, arg):
    """ Zastępuje ciąg znaków w szablonie. Oczekuje formatu 'stary_ciąg,nowy_ciąg'. """
    try:
        # Usuń spacje i podziel argument na dwa ciągi
        old, new = arg.replace(' ', '').split(',')
        return value.replace(old, new)
    except:
        # W przypadku błędu (np. brak przecinka), zwróć oryginalną wartość
        return value