import re

class Parser:
    actions = [
        {
            "name": "price",
            "tag": "span",
            "css_class": "global-styles__TextNoWrap-sc-1gbe8ip-6",
            "function_to_load": "__parse_price"
        },
        {
            "name": "area",
            "tag": "div",
            "css_class": "Tags__TagContainer-sc-edpl7u-0",
            "function_to_load": "__parse_area"
        },
        {
            "name": "region",
            "tag": "span",
            "css_class": "Localizationstyled__City-sc-gdkcr2-1",
            "function_to_load": "__parse_region"
        },
        {
            "name": "code",
            "tag": "span",
            "css_class": "Localizationstyled__City-sc-gdkcr2-1",
            "function_to_load": "__parse_region_code"
        },
        {
            "name": "type",
            "tag": "div",
            "css_class": "Summarystyled__Title-sc-1u9xobv-4",
            "function_to_load": "__parse_type"
        }
    ]

    def __init__(self, content, id: str):
        self.data = {}
        self.content = content[content.index('</head>'):]

        for action in self.actions:
            self.__parse_action(action)

        self.data["id"] = id

    def get_parsed(self) -> dict[str, int|str]:
        return self.data

    def __extract_tag_with_class(self, tag: str, class_name: str) -> str | None:

        pattern = rf'<{tag}[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>'
        match = re.search(pattern, self.content)

        if not match:
            return None

        full_tag_start = match.start()
        tag_close = f'</{tag}>'

        after_tag = self.content[full_tag_start:]
        try:
            content_start = after_tag.index('>') + 1
            content_end = after_tag.index(tag_close)
            return after_tag[content_start:content_end].strip()
        except ValueError:
            return None

    def __parse_action(self, action) -> None:

        name, tag, css_class, function_to_load = action.values()

        raw_content = self.__extract_tag_with_class(tag, css_class)
        if not raw_content:
            return None

        try:
            method = getattr(self.__class__, f"_{self.__class__.__name__}{function_to_load}", None)
            if not method:
                raise AttributeError

            self.data[action["name"]] = method(raw_content)
            return None

        except (ValueError, IndexError, AttributeError):
            return None

    @staticmethod
    def __parse_price(value) -> int:
        value = value[:value.rindex(' ')]
        return int(value.replace(' ', ''))

    @staticmethod
    def __parse_area(value) -> float:
        value = value[:value.rindex(' ')]
        return float(value.replace(' ', ''))

    @staticmethod
    def __parse_region(value) -> str:
        return value[:value.find("(")-1]

    @staticmethod
    def __parse_region_code(value) -> int:
        start = value.find("(")+1
        end = value.find(")", start)
        return int(value[start:end])

    @staticmethod
    def __parse_type(value) -> str:
        return value.split(" ")[0]
