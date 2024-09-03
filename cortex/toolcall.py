import inspect
import json
from typing import Callable, Dict, Any

def function_to_openai_tool(func: Callable) -> Dict[str, Any]:
    """
    Convert a Python function to an OpenAI tool calling definition.

    Args:
        func (Callable): The Python function to convert.

    Returns:
        Dict[str, Any]: OpenAI tool calling definition as a dictionary.
    """
    # Get function signature
    signature = inspect.signature(func)
    
    # Get function docstring
    docstring = inspect.getdoc(func) or ""
    
    # Prepare the tool definition
    tool_definition = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": docstring.split('\n')[0],  # Use first line of docstring as description
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
    
    # Process parameters
    for param_name, param in signature.parameters.items():
        param_info = {
            "type": "string"  # Default to string, you may want to improve this
        }
        
        # Add description if available in docstring
        param_doc = _extract_param_doc(docstring, param_name)
        if param_doc:
            param_info["description"] = param_doc
        
        tool_definition["function"]["parameters"]["properties"][param_name] = param_info
        
        # Check if parameter is required
        if param.default == inspect.Parameter.empty:
            tool_definition["function"]["parameters"]["required"].append(param_name)
    
    return tool_definition

def _extract_param_doc(docstring: str, param_name: str) -> str:
    """
    Extract parameter description from docstring.

    Args:
        docstring (str): The function's docstring.
        param_name (str): The name of the parameter.

    Returns:
        str: The description of the parameter, or an empty string if not found.
    """
    lines = docstring.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith(f":param {param_name}:"):
            return line.split(':', 2)[-1].strip()
    return ""

def openai_to_anthropic_format(openai_tool: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert an OpenAI tool definition to Anthropic format.

    Args:
        openai_tool (Dict[str, Any]): The OpenAI tool definition.

    Returns:
        Dict[str, Any]: The Anthropic format tool definition.
    """
    anthropic_tool = {
        "name": openai_tool["function"]["name"],
        "description": openai_tool["function"]["description"],
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": openai_tool["function"]["parameters"]["required"]
        }
    }

    for param_name, param_info in openai_tool["function"]["parameters"]["properties"].items():
        anthropic_tool["input_schema"]["properties"][param_name] = {
            "type": param_info["type"]
        }
        if "description" in param_info:
            anthropic_tool["input_schema"]["properties"][param_name]["description"] = param_info["description"]
        
        # Check if there's an enum for the parameter
        if "enum" in param_info:
            anthropic_tool["input_schema"]["properties"][param_name]["enum"] = param_info["enum"]

    return anthropic_tool

# Example usage
if __name__ == "__main__":
    def example_function(name: str, age: int, is_student: bool = False):
        """
        An example function to demonstrate the conversion.

        :param name: The name of the person
        :param age: The age of the person
        :param is_student: Whether the person is a student
        """
        pass

    openai_tool = function_to_openai_tool(example_function)
    anthropic_tool = openai_to_anthropic_format(openai_tool)
    print(json.dumps(anthropic_tool, indent=2))

