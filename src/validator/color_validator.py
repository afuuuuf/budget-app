import re

HEX_COLOR_PATTERN = r"#[0-9a-fA-F]{6}"


class ColorValidator:
    @staticmethod
    def hexColorFormatValidation(color: str | None) -> str | None:
        if color is not None and re.fullmatch(HEX_COLOR_PATTERN, color) is None:
            raise ValueError("must be a hex color in #RRGGBB format (e.g. #ff5733)")
        return color
