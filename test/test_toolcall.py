import unittest
from cortex.toolcall import function_to_openai_tool, openai_to_anthropic_format

class TestToolCall(unittest.TestCase):

    def test_function_to_openai_tool(self):
        def sample_function(name: str, age: int, is_student: bool = False):
            """
            A sample function for testing.

            :param name: The name of the person
            :param age: The age of the person
            :param is_student: Whether the person is a student
            """
            pass

        result = function_to_openai_tool(sample_function)
        print(result)
        self.assertEqual(result['type'], 'function')
        self.assertEqual(result['function']['name'], 'sample_function')
        self.assertEqual(result['function']['description'], 'A sample function for testing.')
        
        params = result['function']['parameters']
        self.assertEqual(params['type'], 'object')
        self.assertIn('name', params['properties'])
        self.assertIn('age', params['properties'])
        self.assertIn('is_student', params['properties'])
        
        self.assertEqual(params['properties']['name']['type'], 'string')
        self.assertEqual(params['properties']['name']['description'], 'The name of the person')
        
        self.assertEqual(params['required'], ['name', 'age'])

    def test_openai_to_anthropic_format(self):
        openai_tool = {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                        }
                    },
                    "required": ["location"]
                }
            }
        }

        result = openai_to_anthropic_format(openai_tool)
        print(result)
        self.assertEqual(result['name'], 'get_weather')
        self.assertEqual(result['description'], 'Get the current weather in a given location')
        
        schema = result['input_schema']
        self.assertEqual(schema['type'], 'object')
        self.assertIn('location', schema['properties'])
        self.assertIn('unit', schema['properties'])
        
        self.assertEqual(schema['properties']['location']['type'], 'string')
        self.assertEqual(schema['properties']['location']['description'], 'The city and state, e.g. San Francisco, CA')
        
        self.assertEqual(schema['properties']['unit']['type'], 'string')
        self.assertEqual(schema['properties']['unit']['enum'], ['celsius', 'fahrenheit'])
        
        self.assertEqual(schema['required'], ['location'])

if __name__ == '__main__':
    unittest.main()
