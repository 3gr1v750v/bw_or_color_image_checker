from io import BytesIO
from typing import Union

import requests
from PIL import Image, ImageChops

def download_image(url):
    """
    Скачивание файла и конвертация в битовой формат.

    :param url: Ссылка на изображение
    :type url: str

    :return: Изображение в битовом формате
    :rtype: Union[Image.Image, None]
    """
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def process_image(input_url, percentage_of_error):
    """
    Определение, является картинка черно-белой или нет.

    Берется изображение, конвертируется в черно-белое и сравнивается с
    оригинальной версией. Если разницы нет - возвращает True (т.е.
    оригинал - Черно-белый), если есть - False(т.е. оригинал Цветной).

    Дополнительно реализована допустимая погрешность в процентах. Т.е
    если расхождение состовляет не более 5% (например), то функция возвращает
    True.

    :param url: Ссылка на изображение
    :type url: str

    :param percentage_of_error: Допустимый процент погрешности.
    :type percentage_of_error: int

    :return: True - картинка Ч/Б. False - Цветная
    :rtype: bool
    """
    original_img = download_image(input_url)
    original_img = original_img.convert('RGB')

    img_gray = original_img.convert('L')
    img_gray = img_gray.convert('RGB')

    # Вычисление разницы между изображениями
    diff = ImageChops.difference(original_img, img_gray)

    # Конвертация результатов вычисления в ч/б картинку
    diff_gray = diff.convert('L')

    # Получение значений цветов в пикселях
    diff_data = list(diff_gray.getdata())

    # Общее количество пикселей
    diff_len = len(diff_data)

    # Ссумирование значений цветов
    diff_stat = sum(diff_data)

    # Если условие выполняется - значит картинка Ч/Б, иначе Цветная
    return diff_stat < (percentage_of_error / 100) * diff_len

def main(percentage_of_error, image_url):
    """
    Запуск анализа изображения.

    :param image_url: Ссылка на изображение
    :type image_url: str

    :param percentage_of_error: Допустимый процент погрешности.
    :type percentage_of_error: int

    :return: None
    :rtype: None
    """
    color = ('Черно-белая' if process_image(image_url, percentage_of_error)
             else 'Цветная')

    print(color)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Использование: python main.py <percentage_of_error>, '<image_url>'")
        sys.exit(1)

    percentage_of_error = int(sys.argv[1])
    image_url = sys.argv[2]

    main(percentage_of_error, image_url)
