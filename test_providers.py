import json
import unittest
from unittest.mock import patch
import providers

class ProviderTests(unittest.TestCase):
    def test_missing_key(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError):
                providers.build_request('deepseek','test','hello')

    def test_schemas_and_auth(self):
        for provider, (_, key_name) in providers.PROVIDERS.items():
            with self.subTest(provider=provider), patch.dict('os.environ',{key_name:'test-secret'}):
                req=providers.build_request(provider,'test-model','compressed text',128)
                payload=json.loads(req.data)
                self.assertEqual(payload['model'],'test-model')
                self.assertFalse(payload['stream'])
                self.assertNotIn('test-secret',req.data.decode())
                if provider=='openai':
                    self.assertEqual(payload['input'],'compressed text')
                    self.assertFalse(payload['store'])
                    self.assertEqual(payload['max_output_tokens'],128)
                else:
                    self.assertEqual(payload['messages'][0]['content'],'compressed text')
                    self.assertEqual(payload['max_tokens'],128)

    def test_response_usage_preserved(self):
        response={'choices':[{'message':{'content':'answer'}}],'usage':{'prompt_tokens':10,'completion_tokens':3}}
        with patch.dict('os.environ',{'DEEPSEEK_API_KEY':'test-secret'}), patch('providers.urllib.request.build_opener') as opener:
            opener.return_value.open.return_value.__enter__.return_value.read.return_value=json.dumps(response).encode()
            result=providers.send('deepseek','test','hello')
            self.assertEqual(result['text'],'answer')
            self.assertEqual(result['usage'],response['usage'])
            opener.return_value.open.assert_called_once()

    def test_reject_redirect(self):
        self.assertIsNone(providers.NoRedirect().redirect_request(None,None,302,None,None,'https://example.org'))
