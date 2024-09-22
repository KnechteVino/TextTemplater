import unittest

import texttemplater as tt

class HelperFunctionTests(unittest.TestCase):

    def test_find_before(self):
        text = '121212121'
        self.assertEqual(1, tt._find_before(text, '2', 2))
        self.assertEqual(7, tt._find_before(text, '2', len(text)))
        text = '1212123'
        self.assertEqual(-1, tt._find_before(text, '3', 3))
        
    def test_get_placeholders(self):
        text = '{{one}} some text {{two}} and some {{more}}'
        self.assertSetEqual(set(('one', 'two', 'more')),
                            tt._get_placeholders(text))
        
    def test_find_scope(self):
        text = '[[one scope]] foo {{bar}} [[second scope [[with inner scope]] test]]'
        self.assertEqual((0, 13), tt._find_scope(text), msg=text)
        text = 'foo [[second scope [[with inner scope]] test]]'
        self.assertEqual((4, 46), tt._find_scope(text), msg=text)
        start, end = tt._find_scope(text)
        self.assertEqual('[[second scope [[with inner scope]] test]]', text[start:end])
        texts = ['no scope', 'no [[scope', 'also ]] no [[ scope']
        [self.assertEqual((-1, -1), tt._find_scope(text), msg=text) for text in texts]


class ReplaceTemplateTests(unittest.TestCase):
    
    def test_replace_basic(self):
        template = '{{placeholder}} lorem {{foo}}'
        data = {'placeholder': 'foo', 'foo': 'bar'}
        self.assertEqual('foo lorem bar', tt.replace(template, data))
        
        template = '{{p1}} and [[{{p2}}||or not]]'
        self.assertEqual('true and or not', tt.replace(template, {'p1': 'true'}))
        
        
        template = 'Hello {{name}}, [[you are a {{profession}}||you have no profession]].[[ Also you are {{adj}}!]]'
        solutions = [
            'Hello Nick, you are a programmer. Also you are handsome!',
            'Hello Klaus, you are a manager.',
            'Hello Peter, you have no profession. Also you are useless!'
        ]
        datas = [
            {'name': 'Nick', 'profession': 'programmer', 'adj': 'handsome'},
            {'name': 'Klaus', 'profession': 'manager'},
            {'name': 'Peter', 'adj': 'useless'}
        ]
        for solution, data in zip(solutions, datas):
            self.assertEqual(solution, tt.replace(template, data), msg='{} <=> {}'.format(template, data))
            
    def test_repace_default(self):
        template = '[[Hello [[{{prefix}}||dear]] {{name}}||Dear ladies and gentlemen]]'
        self.assertEqual('Hello dear Jens', tt.replace(template, {'name': 'Jens'}))
        self.assertEqual('Dear ladies and gentlemen', tt.replace(template, {'prefix': 'value'}))
            
    def test_replace_elseblock(self):
        text = '[[{{undefined}}||but {{defined}}]]'
        self.assertEqual('but true', tt.replace(text, {'defined': 'true'}))
        self.assertEqual('delete else', tt.replace(text, {'undefined': 'delete else'}))

        text = '[[{{very-much-nothing}} in scope1 ||[[scope2||foo{{nothing2}}]] bar{{nothing3}}]]'
        self.assertEqual('foo bar', tt.replace(text, {}))

if __name__ == '__main__':
    unittest.main()
