import json

# custom_renderer.py
from rest_framework.renderers import JSONRenderer

def custom_encoder(obj):
    if isinstance(obj, (str, int, float, bool)):
        return str(obj)
    elif isinstance(obj, dict):
        return {str(key): custom_encoder(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [custom_encoder(item) for item in obj]
    else:
        return str(obj)

def convert_error_to_string(data):
    error = json.dumps(custom_encoder(data))
    tok = '[]{}"'
    translation_table = str.maketrans('', '', tok)

    # Remove all brackets using translate
    error = error.translate(translation_table)
    return error

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = data
        status_code = None
        # Extract the status code from the response data, default to 200
        try:
            status_code = data.get('status_code')
        except AttributeError:
            # If data is not dict type and it is list or some other data type, we are
            # converting it to dict
            data = {"data": data}
        if not status_code:
            res = renderer_context.get('response')
            status_code = res.status_code if res else None
        print("data is", data, status_code)
        # Check if the 'error' key is present in the data
        if status_code and int(status_code)//100 in [4,5]:
            # Set the HTTP status code to the extracted status_code for error responses
            status_code = status_code or 400
            renderer_context['response'].status_code = status_code
            error = data.get('error', '') or data
            error = convert_error_to_string(error)
            print(error)
            response_data = {'data': '', 'error': error, 'status_code': int(status_code)}
        elif status_code and int(status_code)//100 in [2,3]:
            # Set the HTTP status code to the extracted status_code for success responses
            renderer_context['response'].status_code = status_code
            response_data = {'data': data.get('data', '') or data, 'error': '', 'status_code': int(status_code)}

        return super().render(response_data, accepted_media_type, renderer_context)
