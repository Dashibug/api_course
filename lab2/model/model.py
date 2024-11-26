import json
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import Dict, Any, Tuple

# Словарь с моделями
MODELS: Dict[str, str] = {
    "RuGPT3Large": "sberbank-ai/rugpt3large_based_on_gpt2",
    "RuGPT3Small": "sberbank-ai/rugpt3small_based_on_gpt2",
    "RuGPT3Medium": "sberbank-ai/rugpt3medium_based_on_gpt2"
}


# Функция для загрузки конфигурации генерации из config.json
def load_generation_params(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Загружает параметры генерации текста из файла конфигурации.

    :param config_path: Путь к файлу конфигурации.
    :return: Словарь с параметрами генерации.
    """
    with open(config_path, "r", encoding="utf-8") as file:
        generation_params = json.load(file)
    return generation_params


# Функция генерации текста с использованием загруженных параметров
def generate_text(model_name: str, input_text: str) -> Tuple[str, float]:
    """
    Генерирует текст на основе выбранной модели и входного текста, используя параметры из конфигурации.

    :param model_name: Имя модели (ключ из словаря MODELS).
    :param input_text: Текст для генерации на его основе.
    :return: Сгенерированный текст и время генерации.
    """
    start_time = time.time()

    # Загрузка модели и токенизатора
    tokenizer = GPT2Tokenizer.from_pretrained(MODELS[model_name])
    model = GPT2LMHeadModel.from_pretrained(MODELS[model_name])

    # Токенизация входного текста
    inputs = tokenizer.encode(input_text, return_tensors="pt")

    # Загрузка параметров генерации из config.json
    generation_params = load_generation_params()

    # Генерация текста с использованием параметров из config.json
    outputs = model.generate(
        inputs,
        do_sample=generation_params.get("do_sample"),
        max_length=generation_params.get("max_length"),
        repetition_penalty=generation_params.get("repetition_penalty"),
        top_k=generation_params.get("top_k"),
        top_p=generation_params.get("top_p"),
        temperature=generation_params.get("temperature"),
        num_beams=generation_params.get("num_beams"),
        no_repeat_ngram_size=generation_params.get("no_repeat_ngram_size")
    )

    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Вычисление времени генерации
    end_time = time.time()
    elapsed_time = end_time - start_time

    return generated_text, elapsed_time
