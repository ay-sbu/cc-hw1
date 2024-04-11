import enum
import hashlib
import re


class Human:
    @classmethod
    def calc_hashed_national_code(cls, national_code: str):
        return hashlib.sha256(national_code.encode()).hexdigest()

    def __init__(self, national_code: str):
        self.hashed_national_code = self.calc_hashed_national_code(national_code)


class Commons(Human):
    def __init__(self, national_code: str, ip: str):
        super().__init__(national_code)
        self.ip = ip


class LocalOfficials(Commons):
    def __init__(self, national_code: str, ip: str):
        super().__init__(national_code, ip)


class CountryOfficials(Commons):
    def __init__(self, national_code: str, ip: str, public_ip: str):
        super().__init__(national_code, ip)
        self.public_ip = public_ip


class Party(int, enum.Enum):
    A = +1
    B = -1


class Area:
    @classmethod
    def ip_pattern_to_regex(cls, ip_pattern: str):
        return re.compile(ip_pattern.replace("X", "\d{1,3}").replace(".", "\."))

    def __init__(self, area_id: str, ip_pattern: str):
        self.ip_pattern = self.ip_pattern_to_regex(ip_pattern)
        self.id = area_id

    def is_ip_in_area_range(self, ip):
        return self.ip_pattern.match(ip) is not None
