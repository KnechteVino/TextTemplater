from texttemplater import replace

if __name__ == '__main__':
    
    #  U S A G E   E X A M P L E S
    
    template = 'Hello {{name}}, [[you are a {{profession}}||you have no profession]][[, and you are {{adjective}}!||.]]{{nevermatch}}'

    data = [
        {'name': 'Nick', 'profession': 'programmer', 'adjective': 'handsome'},
        {'name': 'Klaus', 'profession': 'manager'},
        {'name': 'Peter', 'adjective': 'useless'}
    ]

    print(f'Template:\n{template}\n')
    print('Replaced texts:')
    [print(replace(template, d)) for d in data]

    # beware empty scopes and else blocks
    print()
    templates = [
            '[[Beware empty scopes]]',
            '[[Beware empty scopes {{x}}]]',
            '[[Beware empty scopes [[{{x}}||xxx]]]]'
    ]
    for template in templates:
        print(template, '=>', replace(template, {}))
    template = '[[But if {{y}} then [[{{x}}||xxx]]]]'
    print(template, '=>', replace(template, {'y': 'y'}))
