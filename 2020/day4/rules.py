import fire


def hgt_rule(x):
    try:
        val = int(x[:-2])
        unit = x[-2:]
    except Exception:
        return False

    if unit == 'cm':
        min = 150
        max = 193
    elif unit == 'in':
        min = 59
        max = 76
    else:
        return False

    return min <= val <= max

def hcl_rule(x):
    if x[0] != '#':
        return False

    if len(x[1:]) != 6:
        return False

    try:
        int(x[1:], 16)  # hex check
    except ValueError:
        return False

    return True

RULES = {
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hgt': hgt_rule,
    'hcl': hcl_rule,
    'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda x: len(x) == 9 and x.isnumeric(),
    'cid': lambda x: True,
}
