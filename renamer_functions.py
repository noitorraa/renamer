import os


def is_safe_directory():
    current_dir = os.getcwd()
    unsafe_dirs = ["/", "/root", "/home", "/etc", "/bin", "/usr", "/var"]
    return current_dir not in unsafe_dirs


def get_file_extension(filename):
    if "." in filename:
        return filename.split(".")[-1]
    return ""


def should_rename_file(filename, ext):
    if ext is None:
        print(f"{filename}: ext is None, переименовываем")  # Отладочный вывод
        return True

    file_ext = get_file_extension(filename)
    if not file_ext:
        print(f"{filename}: нет расширения, пропускаем")  # Отладочный вывод
        return False

    result = any(filename.endswith(e) for e in ext)
    print(f"{filename}: file_ext={file_ext}, ext={ext}, result={result}")  # Отладочный вывод
    return result


def generate_new_filename(filename, pattern, counter):
    file_ext = get_file_extension(filename)
    if file_ext:
        return f"{pattern}_{counter}.{file_ext}"
    return f"{pattern}_{counter}"


def rename_files(pattern, ext):
    if not is_safe_directory():
        print("Ошибка: Выполнение в системной директории запрещено.")
        return

    counter = 1
    for filename in os.listdir():
        if not os.path.isfile(filename):
            continue

        if should_rename_file(filename, ext):
            new_name = generate_new_filename(filename, pattern, counter)
            print(f"Переименовываю {filename} в {new_name}")  # Отладочный вывод
            os.rename(filename, new_name)
            counter += 1
