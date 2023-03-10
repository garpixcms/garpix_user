from django.utils import translation


def rupluralize(value, arg='character,characters'):

    lang = translation.get_language()

    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if lang == 'ru':

        if (a == 1) and (b != 11):
            return args[0]
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return args[1]
        else:
            return args[2]

    else:
        if a == 1:
            return args[0]
        else:
            return args[1]
