import datetime
import locale
import sys

LOCALES = {
    'CA': 'ca_ES',
    'CZ': 'cs_CZ',
    'DE': 'de_DE',
    'DK': 'da_DK',
    'EN': 'en_US',
    'ES': 'es_ES',
    'FI': 'fi_FI',
    'FR': 'fr_FR',
    'IS': 'is_IS',
    'GR': 'el_GR',
    'HU': 'hu_HU',
    'IT': 'it_IT',
    'NL': 'nl_NL',
    'PL': 'pl_PL',
    'RO': 'ro_RO',
    'RU': 'ru_RU',
    'SE': 'sv_SE',
    'SI': 'sl_SI',
    'SK': 'sk_SK'
}
VIETNAMESE_DAYS = [
    "chủ nhật", "thứ hai", "thứ ba", "thứ tư", "thứ năm", "thứ sáu", "thứ bảy"
]


def parse_date(d: str):
    (year, month, day) = [int(p) for p in d.split("-")]
    try:
        return datetime.datetime(year, month, day)
    except:
        try:
            return datetime.datetime(day, month, year)
        except:
            return None


def solve():
    results = []
    for line in sys.stdin:
        if ':' in line:
            (string_date, string_locale) = line.strip().split(':')
            date = parse_date(string_date)
            if date is None:
                results.append("INVALID_DATE")
            elif string_locale == 'VI':
                results.append(VIETNAMESE_DAYS[int(date.strftime('%w'))])
            elif string_locale not in LOCALES:
                results.append("INVALID_LANGUAGE")
            else:
                locale.setlocale(locale.LC_ALL, LOCALES[string_locale])
                results.append(date.strftime('%A').lower())

    for (i, result) in enumerate(results):
        print("Case #{}: {}".format(i + 1, result))


if __name__ == '__main__':
    solve()
