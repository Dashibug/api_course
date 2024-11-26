import tkinter as tk
from tkinter import ttk
from model.model import generate_text  # Импорт функции генерации текста
from model.model import MODELS  # Импорт словаря моделей


# Создание интерфейса
def create_interface() -> None:
    """
    Создает графический интерфейс для генерации текста с использованием RuGPT.
    """
    root = tk.Tk()
    root.title("Text Generation with RuGPT")

    # Выбор модели
    model_label = ttk.Label(root, text="Choose a model:")
    model_label.pack(pady=5)

    model_var = tk.StringVar()
    model_combobox = ttk.Combobox(root, textvariable=model_var, values=list(MODELS.keys()), state="readonly")
    model_combobox.pack(pady=5)
    model_combobox.current(0)  # Установка модели по умолчанию

    # Ввод текста
    input_text_label = ttk.Label(root, text="Input Text:")
    input_text_label.pack(pady=5)

    input_text_box = tk.Text(root, height=10, width=50)
    input_text_box.pack(pady=5)

    # Кнопка для генерации текста
    generate_button = ttk.Button(root, text="Generate", command=lambda: on_generate(model_var.get(), input_text_box.get("1.0", tk.END).strip()))
    generate_button.pack(pady=10)

    # Поле для отображения результата
    global result_text_box
    result_text_box = tk.Text(root, height=10, width=50, state=tk.DISABLED)
    result_text_box.pack(pady=5)

    # Запуск приложения
    root.mainloop()


def on_generate(model_name: str, input_text: str) -> None:
    """
    Обрабатывает нажатие кнопки генерации текста, генерирует текст на основе входного текста и выбранной модели.

    :param model_name: Имя выбранной модели.
    :param input_text: Входной текст для генерации.
    """
    if model_name and input_text:  # Проверка наличия модели и текста
        generated_text, elapsed_time = generate_text(model_name, input_text)

        # Вывод результата
        result_text_box.config(state=tk.NORMAL)  # Разрешить редактирование
        result_text_box.delete("1.0", tk.END)  # Очистка предыдущего текста
        result_text_box.insert(tk.END,
                               f"\n{generated_text}\n\nTime Taken: {elapsed_time:.2f} seconds")  # Вставка нового текста
        result_text_box.config(state=tk.DISABLED)  # Запретить редактирование
