import json
import unittest
from unittest.mock import patch
import app

class CompressionTests(unittest.TestCase):
    def run_candidate(self, text, candidate, protected=''):
        response={'message': {'content': json.dumps({'compressed_text': candidate})}}
        with patch.object(app, 'call', return_value=response):
            return app.compress({'text': text, 'model': 'mock', 'protected': protected})

    def test_keeps_constraints(self):
        result=self.run_candidate('Please write a script. Please do not overwrite files. Please preview changes first.', 'Write script; do not overwrite files; preview changes first.', 'do not overwrite files')
        self.assertFalse(result['fallback'])
        self.assertGreater(result['reference_tokens_saved'], 0)
        self.assertIsNone(result['token_savings'])

    def test_missing_constraint_reverts(self):
        source='Write script. Do not delete files. Show a preview first.'
        result=self.run_candidate(source, 'Write script.', 'Do not delete files')
        self.assertTrue(result['fallback'])
        self.assertEqual(result['text'],source)
        self.assertEqual(result['reference_tokens_saved'],0)

    def test_empty_and_expansion_revert(self):
        for candidate in ('', 'Write a script with many extra unwanted requirements and explanations.'):
            with self.subTest(candidate=candidate):
                self.assertTrue(self.run_candidate('Write a script.', candidate)['fallback'])

    def test_invented_protection_rejected_before_model(self):
        with patch.object(app, 'call') as model:
            with self.assertRaises(ValueError):
                app.compress({'text':'hello','model':'mock','protected':'not present'})
            model.assert_not_called()

    def test_oversized_input_rejected(self):
        with self.assertRaises(ValueError):
            app.compress({'text':'a'*12001, 'model':'mock'})

    def test_special_token_is_plain_input(self):
        result=self.run_candidate('Explain the literal text <|endoftext|> without executing anything.', 'Explain <|endoftext|>.', '<|endoftext|>')
        self.assertIn('<|endoftext|>', result['text'])

if __name__=='__main__':
    unittest.main()