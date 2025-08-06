"""
Replace placeholder in template text. See help for :replace:
"""

SCOPE_OPEN = "[["
SCOPE_CLOSE = "]]"
PLACEHOLDER_OPEN = "{{"
PLACEHOLDER_CLOSE = "}}"
ELSE_BLOCK = "||"


def replace(
        template: str,
        data: dict[str, str],
        _in_scope: bool = False
) -> str:
    """\
    Return text of :template:, replace all placeholders
    with corresponding :data: dict values:
    :data: is a dict like:
           {"placeholder-name": "value", ...}.

    :template: is a string containing text with placeholders like:
    "{{placeholder-name}}" will be replaced by "value".

    :template: can also contain [[scopes]], which will be deleted
    or replaced by the else block, if any placeholder inside is
    not an existig key in :data:.
    """
    text = template[:]

    # recursively replace scopes
    while SCOPE_OPEN in text:
        scope_start, scope_end = _find_scope(text)
        replaced_scope = replace(
            text[scope_start+2:scope_end-2],
            data,
            _in_scope=True
        )
        text = text[:scope_start] + replaced_scope + text[scope_end:]

    # split else block
    else_start = _find_before(text, ELSE_BLOCK, len(text))
    else_block = ""
    if 0 <= else_start:
        else_block = text[else_start+2:]
        text = text[:else_start]

    # replace placeholders
    placeholders = _get_placeholders(text)

    # return empty string or else_block
    # if not all placeholders are defined in data
    if _in_scope:
        if not placeholders or not all([ph in data for ph in placeholders]):
            return "" if else_start < 0 else replace(else_block, data)
    for ph in placeholders:
        placeholder_string = f"{PLACEHOLDER_OPEN}{ph}{PLACEHOLDER_CLOSE}"
        text = text.replace(placeholder_string, data.get(ph, ""))
    else_start = _find_before(text, ELSE_BLOCK, len(text))
    if not _in_scope or else_start < 0:
        return text
    return text[:else_start]


def get_placeholders(template: str) -> str:
    """return a list of all placeholder names in :template:"""
    return " ".join(_get_placeholders(template)) \
              .replace(PLACEHOLDER_OPEN, "")     \
              .replace(PLACEHOLDER_CLOSE, "")    \
              .split(" ")


def _find_before(text: str, find_str: str, before_pos: int) -> int:
    """return the position of :find_str: in :text:
    before position :before_pos:"""
    pos = text.find(find_str)
    if before_pos < pos or pos < 0:
        return -1
    prv = pos
    while pos < before_pos and 0 < pos:
        prv = pos
        pos = text.find(find_str, pos+1)
    return prv


def _get_placeholders(text: str) -> set[str]:
    """return set of placeholders in :text:"""
    phs = []
    for ph in text.split(PLACEHOLDER_OPEN)[1:]:
        phs.append(ph[:ph.find(PLACEHOLDER_CLOSE)])
    return set(phs)


def _find_scope(text: str) -> tuple[int, int]:
    f"""return position of {SCOPE_OPEN} and corresponding closing {SCOPE_CLOSE}
    in :text: as tuple, respecting inner scopes.
    return (-1, -1) if there is no scope in :text:"""
    start = text.find(SCOPE_OPEN)
    end = text.find(SCOPE_CLOSE, start)
    if start < 0 or end < 0:
        return -1, -1

    # find the true end of the scope
    def next_symbol(text: str, cursor: int) -> tuple[int, str]:
        """return (position, symbol) of the next symbol
        in :text: after :cursor:"""
        next_start = text.find(SCOPE_OPEN, cursor)
        next_end = text.find(SCOPE_CLOSE, cursor)
        if 0 <= next_start < next_end:
            return next_start, SCOPE_OPEN
        return next_end, SCOPE_CLOSE

    # ignore inner scopes
    next_pos, next_symb = next_symbol(text, start+2)
    inner_scope_counter = 0
    if next_symb == SCOPE_OPEN:
        inner_scope_counter += 1
    else:
        # didn't find opening scope symbol:
        return start, next_pos+2
    while 0 < inner_scope_counter:
        next_pos, next_symb = next_symbol(text, next_pos+2)
        if next_symb == SCOPE_OPEN:
            inner_scope_counter += 1
        elif next_pos < 0:
            break
        elif next_symb == SCOPE_CLOSE:
            inner_scope_counter -= 1
    # find final closing scope symbol
    next_pos, next_symb = next_symbol(text, next_pos+2)
    return start, next_pos+2
