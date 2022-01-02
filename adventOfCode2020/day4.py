import sys
from typing import Dict


def validate_passport_data(passport: Dict[str, str]) -> bool:
    expected_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    got_keys = set(passport.keys())
    return expected_keys.intersection(got_keys) == expected_keys


def validate_passport_data_extended(passport: Dict[str, str]) -> bool:
    if not validate_passport_data(passport):
        return False

    byr = int(passport["byr"])
    if not (1920 <= byr <= 2002):
        return False

    iyr = int(passport["iyr"])
    if not (2010 <= iyr <= 2020):
        return False

    eyr = int(passport["eyr"])
    if not (2020 <= eyr <= 2030):
        return False

    hgt = passport["hgt"]
    if "cm" in hgt:
        hgt = int(hgt.replace("cm", ""))
        if not (150 <= hgt <= 193):
            return False
    elif "in" in hgt:
        hgt = int(hgt.replace("in", ""))
        if not (59 <= hgt <= 76):
            return False
    else:
        return False

    if passport["hcl"][0] == "#" and len(passport["hcl"]) == 7:
        try:
            _ = int(passport["hcl"][1:], 16)
        except ValueError:
            return False
    else:
        return False

    if passport["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    if len(passport["pid"]) == 9:
        try:
            _ = int(passport["pid"])
        except ValueError:
            return False
    else:
        return False

    return True


def solve():
    passports = []
    current_passport = {}
    for line in sys.stdin.readlines():
        if line.strip() == "":
            passports.append(current_passport)
            current_passport = {}
        else:
            kv_pairs = line.strip().split(" ")
            for kv in kv_pairs:
                key, value = kv.split(":")
                current_passport[key] = value
    passports.append(current_passport)

    if sys.argv[1] == 'part1':
        return sum(int(validate_passport_data(p)) for p in passports)
    if sys.argv[1] == 'part2':
        return sum(int(validate_passport_data_extended(p)) for p in passports)


if __name__ == '__main__':
    print(solve())
