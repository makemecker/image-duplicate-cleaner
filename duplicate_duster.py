import argparse
import hashlib
import os
from collections import defaultdict

from tqdm import tqdm


def check_image_path(path: str):
    """ Валидация указанного пути к папке с изображениями"""

    if not isinstance(path, str):
        print("Ошибка: Путь к изображениям (image_path) должен быть указан в виде строки.")
        return False
    if not os.path.exists(path):
        print("Ошибка: Указанного пути к изображениям не существует.")
        return False
    if not os.listdir(path):
        print(
            "Предупреждение: Папка с изображениями (image_path) пуста. Рекомендуется добавить изображения перед "
            "запуском функции.")
        return False
    return True


def calculate_hash(file_path):
    """Вычисляет MD5 хэш файла"""

    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_dupls(duplicate_image_dir: str) -> int | None:
    """ Удаляет изображения-дубликаты"""

    if not check_image_path(duplicate_image_dir):
        return

    all_image_exts = {".jpeg", ".jpg", ".png", ".tiff", ".gif", ".bmp", ".raw", ".heic", ".webp"}
    counter = 0

    image_hashes = defaultdict(list)
    for image in [file for file in os.listdir(duplicate_image_dir) if os.path.splitext(file)[1] in all_image_exts]:
        cur_img_path = os.path.join(duplicate_image_dir, image)
        image_hashes[calculate_hash(cur_img_path)].append(cur_img_path)

    for hash_value, duplicates in tqdm(image_hashes.items()):
        if len(duplicates) > 1:
            for duplicate in duplicates[1:]:
                os.remove(duplicate)
                counter += 1

    return counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate images.")
    parser.add_argument("--image_dir", required=True, help="Path to the folder containing images.")
    args = parser.parse_args()
    image_dir_arg = args.image_dir

    rm_dupl_count = remove_dupls(duplicate_image_dir=image_dir_arg)

    if rm_dupl_count:
        print(f"Deleted {rm_dupl_count} duplicate images.")
    else:
        print("No duplicate images found.")
