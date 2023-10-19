import requests
import openai

from typing import Union, List
from apps.keymanagement.models import LLMProviders
from apps.library.models import PromptTypeEnum, Prompt, PromptOutput, PromptVariable
from .constants import DefaultParametersValues

class LLMService:
    def completion(self, prompt):
        raise NotImplementedError("Subclasses must implement the completion method")

    def chat(self, messages):
        raise NotImplementedError("Subclasses must implement the chat method")


class OpenAIProvider(LLMService):
    def __init__(self, prompt):
        self.prompt = prompt
        self.api_key = prompt.workspace.model_key.api_key

    def run(self):
        if self.prompt.prompt_type == PromptTypeEnum.CHAT.value:
            self.chat()
        elif self.prompt.prompt_type == PromptTypeEnum.COMPLETION.value:
            self.completion()

    def completion(self):
        parameters = self.prompt.parametermapping_set.all()

        temperature = parameters.filter(parameter__name="temperature").first()
        temperature = float(temperature.value) if temperature else DefaultParametersValues.temperature

        max_tokens = parameters.filter(parameter__name="max_tokens").first()
        max_tokens = int(max_tokens.value) if max_tokens else DefaultParametersValues.max_tokens

        top_p = parameters.filter(parameter__name="top_p").first()
        top_p = float(top_p.value) if top_p else DefaultParametersValues.top_p

        frequency_penalty = parameters.filter(
            parameter__name="frequency_penalty"
        ).first()
        frequency_penalty = float(frequency_penalty.value) if frequency_penalty else DefaultParametersValues.frequency_penalty

        presence_penalty = parameters.filter(parameter__name="presence_penalty").first()
        presence_penalty = float(presence_penalty.value) if presence_penalty else DefaultParametersValues.presence_penalty

        logit_bias = parameters.filter(parameter__name="logit_bias").first()
        logit_bias = dict(logit_bias.value) if logit_bias else DefaultParametersValues.logit_bias
        decoded_user_message = decode_user_message(self.prompt)
        openai.api_key = self.api_key
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=decoded_user_message,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logit_bias=logit_bias,
        )
        data = response.to_dict()
        ai_response = data["choices"][0]["text"]
        PromptOutput.objects.create(
            prompt=self.prompt, output=ai_response
        )
        return

    def chat(self):
        parameters = self.prompt.parametermapping_set.all()

        temperature = parameters.filter(parameter__name="temperature").first()
        temperature = float(temperature.value) if temperature else DefaultParametersValues.temperature

        max_tokens = parameters.filter(parameter__name="max_tokens").first()
        max_tokens = int(max_tokens.value) if max_tokens else DefaultParametersValues.max_tokens

        top_p = parameters.filter(parameter__name="top_p").first()
        top_p = float(top_p.value) if top_p else DefaultParametersValues.top_p

        frequency_penalty = parameters.filter(
            parameter__name="frequency_penalty"
        ).first()
        frequency_penalty = float(frequency_penalty.value) if frequency_penalty else DefaultParametersValues.frequency_penalty

        presence_penalty = parameters.filter(parameter__name="presence_penalty").first()
        presence_penalty = float(presence_penalty.value) if presence_penalty else DefaultParametersValues.presence_penalty

        logit_bias = parameters.filter(parameter__name="logit_bias").first()
        logit_bias = dict(logit_bias.value) if logit_bias else DefaultParametersValues.logit_bias

        messages = []
        messages.append({"role": "system", "content": self.prompt.system_message})
        past_prompts = Prompt.objects.filter(
            workspace=self.prompt.workspace, prompt_type=PromptTypeEnum.CHAT.value
        ).exclude(id=self.prompt.id)
        # considering only last 10 prompts for chat, to avoid large payload and slow response
        for prompt in list(past_prompts)[-10:]:
            decoded_user_message = decode_user_message(prompt)
            messages.append({"role": "user", "content": decoded_user_message})
            messages.append({"role": "assistant", "content": prompt.sample_output})
        decoded_user_message = decode_user_message(self.prompt)
        messages.append({"role": "user", "content": decoded_user_message})
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logit_bias=logit_bias,
        )
        data = response.to_dict()
        ai_response = data["choices"][0]["message"]["content"]
        PromptOutput.objects.create(
            prompt=self.prompt, output=ai_response
        )
        return


class BardProvider(LLMService):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = (
            "https://api.bard.com/v1"  # Replace with the actual Bard API URL
        )

    def completion(
        self,
        prompt,
        temperature=1.0,
        max_length=50,
        stop_sequence=None,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        logit_bias=None,
    ):
        url = f"{self.base_url}/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": temperature,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "top_p": top_p,
            "stop_sequence": stop_sequence,
            "logit_bias": logit_bias,
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data["choices"][0]["text"]

    def chat(
        self,
        messages,
        temperature=1.0,
        max_length=50,
        stop_sequence=None,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        logit_bias=None,
    ):
        url = f"{self.base_url}/engines/bard-chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": [{"role": "system", "content": "You are a helpful assistant."}],
            "max_tokens": max_length,
            "temperature": temperature,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "top_p": top_p,
            "stop_sequence": stop_sequence,
            "logit_bias": logit_bias,
        }
        for message in messages:
            data["messages"].append({"role": "user", "content": message})
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]


class LLMServiceFactory:
    @staticmethod
    def create_llm_service(prompt) -> Union[OpenAIProvider, BardProvider]:
        provider_type = prompt.workspace.model_key.provider
        if provider_type == LLMProviders.OPENAI.value:
            return OpenAIProvider(prompt)
        elif provider_type == LLMProviders.BARD.value:
            return BardProvider(prompt)
        else:
            raise ValueError("Invalid LLM provider type")

def decode_user_message(prompt: Prompt) -> str:
    user_message = prompt.user_message
    variables: List[PromptVariable] = prompt.promptvariable_set.all()
    for variable in variables:
        key = variable.key
        value = variable.value
        user_message = user_message.replace("{{" + key + "}}", value)
    return user_message
