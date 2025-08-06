"""
Replace placeholder in template text. See help for :replace:
"""

def replace(template, data, _in_scope=False):
    """
    Returns text of :template: where all placeholder
    are replaced with corresponding :data: dict values:
    :data: is a dict like
           {'placeholder-name': 'value', ...}.
    
    :template: is a string containing text and placeholders like:
    {{placeholder-name}} will be replaced by 'value'.
    
    :template: can also contain [[scopes]], which will be deleted
    or replaced by the else block, if any placeholder inside is
    not a key in :data:.
    """
    text = template[:]
    # recursive replace scopes
    while '[[' in text:
        scope_start, scope_end = _find_scope(text)
        text = text[:scope_start] + replace(text[scope_start+2:scope_end-2], data, _in_scope=True) + text[scope_end:]
    # split else block
    else_start = _find_before(text, '||', len(text))
    else_block = '' 
    if 0 <= else_start:
        else_block = text[else_start+2:]
        text = text[:else_start]
    
    # replace placeholders
    placeholders = _get_placeholders(text)
    if _in_scope: # return empty string or else_block if not all placeholders are defined in data
        if not placeholders or not all([ph in data for ph in placeholders]):
            return '' if else_start < 0 else replace(else_block, data)
    for ph in placeholders:
        text = text.replace('{{'+ph+'}}', data.get(ph, ''))
    else_start = _find_before(text, '||', len(text))
    if not _in_scope or else_start < 0:
        return text
    return text[:else_start]

def get_placeholders(template):
    """returns a list of all placeholder names in :template:"""
    return " ".join(_get_placeholders(template)) \
              .replace('{{', '').replace('}}', '').split(' ')

def _find_before(text, find_str, before_pos):
    """returns the position of :find_str: in :text:
    before position :before_pos:"""
    pos = text.find(find_str)
    if before_pos < pos or pos < 0:
        return -1
    prv = pos
    while pos < before_pos and 0 < pos:
        prv = pos
        pos = text.find(find_str, pos+1)
    return prv

def _get_placeholders(text):
    """returns a list of placeholders in text"""
    phs = []
    for ph in text.split('{{')[1:]:
        phs.append(ph[:ph.find('}}')])
    return set(phs)

def _find_scope(text):
    """returns position of "[[" and corresponding closing "]]"
    in :text: as tuple, respecting inner scopes.
    returns (-1, -1) if there is no scope in :text:"""
    start = text.find('[[')
    end = text.find(']]', start)
    if start < 0 or end < 0:
        return -1, -1
    
    def next_symbol(text, cursor):
        """returns (position, symbol) of the next symbol
        in :text: after :cursor:"""
        next_start = text.find('[[', cursor)
        next_end = text.find(']]', cursor)
        if 0 <= next_start < next_end:
            return next_start, '[[' 
        return next_end, ']]'
    
    next_pos, next_symb = next_symbol(text, start+2)
    inner_scope_counter = 0
    if next_symb == '[[':
        inner_scope_counter += 1
    else: # didn't find new opening scope symbol:
        return start, next_pos+2
    
    while 0 < inner_scope_counter:
        next_pos, next_symb = next_symbol(text, next_pos+2)
        if next_symb == '[[':
            inner_scope_counter += 1
        elif next_pos < 0:
            break
        elif next_symb == ']]':
            inner_scope_counter -= 1
    # find final closing scope symbol
    next_pos, next_symb = next_symbol(text, next_pos+2)
    return start, next_pos+2

