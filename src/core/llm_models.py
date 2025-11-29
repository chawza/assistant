from pydantic_ai.models.openai import OpenAIChatModel, Model
from pydantic_ai.providers.ollama import OllamaProvider
import tomllib

model_dicts = tomllib.load(open("models.toml", "rb"))

def get_model(model_name: str) -> Model:
    model_dict = model_dicts[model_name]

    match model_dict['vendor']:
        case 'ollama':
            return OpenAIChatModel(
                model_name=model_dict['model'],
                provider=OllamaProvider(
                    base_url=model_dict['base_url'],
                    api_key=model_dict['api_key']
                ),
            )
        case _:
            raise AttributeError(f"Unsupported vendor: {model_dict['vendor']}")
