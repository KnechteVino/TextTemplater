# TextTemplater
is **not** a web template engine. It is used for sending automated serial letter emails.

## Simple Text Templating:
Replace placeholders in a text template, supporting optional placeholders and scopes.

Template example:

```
[[Dear {{prefix}} {{surname}}||Hello]], lorem ipsum...
```

* `{{placeholder}}` will be replaced with a provided value.
* `[[...]]` is a scope. Text inside scope is only shown if all placeholders in this scope have values.
* `[[...||elseblock]]` is a scope with an else-block. If any placeholder in this scope is missing, the scope will be replaced by the contents of the elseblock.

## Examples:

```python

import texttemplater

template = 'Hello {{name}}, [[you are a {{profession}}||you have no profession]].[[ Also you are {{adjective}}!]]'

data = [
    {'name': 'Nick', 'profession': 'programmer', 'adjective': 'handsome'},
    {'name': 'Klaus', 'profession': 'manager'},
    {'name': 'Peter', 'adjective': 'useless'}
]

[print(texttemplater.replace(template, data)) for data in datas]
```

Results in:

```
Hello Nick, you are a programmer. Also you are handsome!
Hello Klaus, you are a manager.
Hello Peter, you have no profession. Also you are useless!
```

Use nested scopes to create optional placeholders in a scope:

```python
template = '[[Hello [[{{prefix}}||dear]] {{name}}||Dear ladies and gentlemen]]'

print(texttemplater.replace(template, {'name': 'Jens'}))
```

Results in:

```
Hello dear Jens
```
