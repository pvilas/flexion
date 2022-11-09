#!/usr/bin/env python

# original: https://github.com/bermi/Python-Inflector
# adapted by Pere Vilás https://github.com/pvilas/flexion


import re

irregular_words = {
    u'base': u'bases',
    u'carácter': u'caracteres',
    u'champú': u'champús',
    u'curriculum': u'currículos',
    u'espécimen': u'especímenes',
    u'jersey': u'jerséis',
    u'memorándum': u'memorandos',
    u'menú': u'menús',
    u'no': u'noes',
    u'país': u'países',
    u'referéndum': u'referendos',
    u'régimen': u'regímenes',
    u'sándwich': u'sándwiches',
    u'si': u'sis', # Nota musical ALERTA: ¡provoca efectos secundarios!
    u'taxi': u'taxis', 
    u'ultimátum': u'ultimatos',
    }

# These words either have the same form in singular and plural, or have no singular form at all
non_changing_words = [
    u'lunes', u'martes', u'miércoles', u'jueves', u'viernes',
    u'paraguas', u'tijeras', u'gafas', u'vacaciones', u'víveres',
    u'cumpleaños', u'virus', u'atlas', u'sms', u'hummus',
]


def string_replace(word, find, replace):
    '''This function returns a copy of word, translating
    all occurrences of each character in find to the
    corresponding character in replace'''
    for k in range(0, len(find)):
        word = re.sub(find[k], replace[k], word)

    return word


def pluraliza(word):
    '''
    Pluralizes Spanish nouns.
    '''

    rules = [
        [u'(?i)([aeiou])x$', u'\\1x'],
        # This could fail if the word is oxytone.
        [u'(?i)([áéíóú])([ns])$', u'|1\\2es'],
        [u'(?i)(^[bcdfghjklmnñpqrstvwxyz]*)an$', u'\\1anes'],  # clan->clanes
        [u'(?i)([áéíóú])s$', u'|1ses'],
        [u'(?i)(^[bcdfghjklmnñpqrstvwxyz]*)([aeiou])([ns])$', u'\\1\\2\\3es'],  # tren->trenes
        [u'(?i)([aeiouáéó])$', u'\\1s'],  # casa->casas, padre->padres, papá->papás
        [u'(?i)([aeiou])s$', u'\\1s'],    # atlas->atlas, virus->virus, etc.
        [u'(?i)([éí])(s)$', u'|1\\2es'],  # inglés->ingleses
        [u'(?i)z$', u'ces'],              # luz->luces
        [u'(?i)([íú])$', u'\\1es'],       # ceutí->ceutíes, tabú->tabúes
        [u'(?i)(ng|[wckgtp])$', u'\\1s'], # Anglicismos como puenting, frac, crack, show (En que casos podría fallar esto?)
        [u'(?i)$', u'es']  # ELSE +es (v.g. árbol->árboles)
    ]

    lower_cased_word = word.lower()

    for uncountable_word in non_changing_words:
        if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
            return word            

    for irregular_singular, irregular_plural in irregular_words.items():
        match = re.search(u'(?i)(^' + irregular_singular + u')$', word, re.IGNORECASE)
        if match:
            result = re.sub(u'(?i)' + irregular_singular + u'$', match.expand(u'\\1')[0] + irregular_plural[1:], word)
            return result

    for rule in rules:
        match = re.search(rule[0], word, re.IGNORECASE)
        if match:
            groups = match.groups()
            replacement = rule[1]
            if re.match(u'\|', replacement):
                for k in range(1, len(groups)):
                    replacement = replacement.replace(u'|' + k,
                          string_replace(groups[k - 1], u'ÁÉÍÓÚáéíóú', u'AEIOUaeiou'))

            result = re.sub(rule[0], replacement, word)
            # Esto acentúa los sustantivos que al pluralizarse se
            # convierten en esdrújulos como esmóquines, jóvenes...
            match = re.search(u'(?i)([aeiou]).{1,3}([aeiou])nes$', result)

            if match and len(match.groups()) > 1 and not re.search(u'(?i)[áéíóú]', word):
                result = result.replace(match.group(0), string_replace(
                    match.group(1), u'AEIOUaeiou', u'ÁÉÍÓÚáéíóú') + match.group(0)[1:])

            return result

    return word


def singulariza(word):
    '''
    Singularizes Spanish nouns.
    '''

    rules = [
        [u'(?i)^([bcdfghjklmnñpqrstvwxyz]*)([aeiou])([ns])es$', u'\\1\\2\\3'],
        [u'(?i)([aeiou])([ns])es$', u'~1\\2'],
        [u'(?i)shes$', u'sh'],             # flashes->flash
        [u'(?i)oides$', u'oide'],          # androides->androide
        [u'(?i)(sis|tis|xis)$', u'\\1'],   # crisis, apendicitis, praxis
        [u'(?i)(é)s$', u'\\1'],            # bebés->bebé
        [u'(?i)(ces)$', u'z'],             # luces->luz
        [u'(?i)([^e])s$', u'\\1'],         # casas->casa
        [u'(?i)([bcdfghjklmnñprstvwxyz]{2,}e)s$', u'\\1'],  # cofres->cofre
        [u'(?i)([ghñptv]e)s$', u'\\1'],    # llaves->llave, radiocasetes->radiocasete
        [u'(?i)jes$', u'je'],              # ejes->eje
        [u'(?i)ques$', u'que'],            # tanques->tanque
        [u'(?i)es$', u'']                  # ELSE remove _es_  monitores->monitor
    ]

    lower_cased_word = word.lower()

    for uncountable_word in non_changing_words:
        if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
            return word

    for irregular_singular, irregular_plural in irregular_words.items():
        match = re.search(u'(^' + irregular_plural + u')$', word, re.IGNORECASE)
        if match:
            result = re.sub(u'(?i)' + irregular_plural + u'$', match.expand(u'\\1')[0] + irregular_singular[1:], word)
            return result

    for rule in rules:
        match = re.search(rule[0], word, re.IGNORECASE)
        if match:
            groups = match.groups()
            replacement = rule[1]
            if re.match(u'~', replacement):
                for k in range(1, len(groups)):
                    replacement = replacement.replace(u'~' + k, string_replace(groups[k - 1], u'AEIOUaeiou', u'ÁÉÍÓÚáéíóú'))

            result = re.sub(rule[0], replacement, word)
            # Esta es una posible solución para el problema de dobles
            # acentos. Un poco guarrillo pero funciona
            match = re.search(u'(?i)([áéíóú]).*([áéíóú])', result)

            if match and len(match.groups()) > 1 and not re.search(u'(?i)[áéíóú]', word):
                result = string_replace(
                    result, u'ÁÉÍÓÚáéíóú', u'AEIOUaeiou')

            return result

    return word
