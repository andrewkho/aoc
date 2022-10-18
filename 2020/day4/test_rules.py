import pytest

import rules

@pytest.mark.parametrize(
    'rule, input, expected',
    [
        ['byr', '1900', False],
        ['byr', '1920', True],
        ['byr', '1930', True],
        ['byr', '2002', True],
        ['byr', '3000', False],

        ['iyr', '1900', False],
        ['iyr', '2010', True],
        ['iyr', '2015', True],
        ['iyr', '2020', True],
        ['iyr', '3000', False],

        ['eyr', '1900', False],
        ['eyr', '2020', True],
        ['eyr', '2025', True],
        ['eyr', '2030', True],
        ['eyr', '3000', False],

        ['hgt', '1asdf', False],
        ['hgt', '150cm', True],
        ['hgt', '193cm', True],
        ['hgt', '59in', True],
        ['hgt', '76in', True],
        ['hgt', '59cm', False],
        ['hgt', '76cm', False],
        ['hgt', '150in', False],
        ['hgt', '193in', False],

        ['hcl', 'asdf', False],
        ['hcl', '#a987df', True],
        ['hcl', '#a987df7', False],
        ['hcl', '#o83848', False],

        ['ecl', 'amb', True],
        ['ecl', 'blu', True],
        ['ecl', 'brn', True],
        ['ecl', 'gry', True],
        ['ecl', 'grn', True],
        ['ecl', 'hzl', True],
        ['ecl', 'oth', True],
        ['ecl', 'abc', False],

        ['pid', '012345678', True],
        ['pid', '0123456789', False],
        ['pid', '123456789', True],
    ]
)
def test_rules(rule: str, input: str, expected: bool):
    rule = rules.RULES[rule]
    
    assert rule(input) == expected

