import typing

from wolai.types.enum import AutoName, auto


class NumberFormats(AutoName):
    yen = auto()
    vnd = auto()
    hkd = auto()
    euro = auto()
    yuan = auto()
    float = auto()
    pound = auto()
    dollar = auto()
    number = auto()
    percent = auto()
    integer = auto()
    progress = auto()
    thousandth = auto()


class PropertyType(AutoName):
    sn = auto()
    url = auto()
    text = auto()
    date = auto()
    file = auto()
    email = auto()
    phone = auto()
    people = auto()
    rollup = auto()
    select = auto()
    number = auto()
    primary = auto()
    formula = auto()
    checkbox = auto()
    relation = auto()
    edited_by = auto()
    created_by = auto()
    edited_time = auto()
    created_time = auto()
    multi_select = auto()


class PropertyFileInfo:
    download_url: str = None
    expires_in: int = None
    is_image: bool = False

    def __init__(self, download_url: str = None, expires_in: int = -1, is_image: bool = False):
        self.download_url = download_url
        self.expires_in = expires_in
        self.is_image = is_image


class PropertyValue:
    type: PropertyType = None
    value: str = None
    number_format: NumberFormats = None
    file_info: list[PropertyFileInfo] = None

    def __init__(self, type: PropertyType | str, value: str, number_format: NumberFormats | str = None,
                 file_list: list[PropertyFileInfo] = None):
        if isinstance(type, str):
            type = PropertyType[type]

        self.type = type
        self.value = value

        if isinstance(number_format, str):
            number_format = NumberFormats[number_format]

        self.number_format = number_format
        self.file_info = file_list


class CreateDatabaseRow(dict):
    pass


class DatabaseRowData:
    data: dict[str:PropertyValue] = None

    def __init__(self, data: dict[str:PropertyValue] | dict[str:dict] = None, **kwargs):
        new_data: dict[str:PropertyValue] = {}
        for k, v in data.items():
            if isinstance(v, dict):
                v = PropertyValue(**v)
            elif isinstance(v, PropertyValue):
                v = v
            else:
                continue

            new_data[k] = v
        self.data = new_data

    def __repr__(self):
        return self.data

    def to_create_database_row(self) -> CreateDatabaseRow:
        data = {}
        for k, v in self.data.items():
            data[k] = v.value

        return CreateDatabaseRow(data)
