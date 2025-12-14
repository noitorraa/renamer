import renamer_functions
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Утилита для массового переименования файлов в директории по шаблону"
    )
    parser.add_argument(
        "--pattern",
        dest="pattern",
        type=str,
        required=True,
        help="Ввести паттерн для переименования файлов",
    )
    parser.add_argument(
        "--extension",
        dest="ext",
        nargs="+",
        required=False,
        help="Выбор расширений для файлов, которые будут переименованы, если не выбрать, то будут периименованы все файлы в директории",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    # Если --extension не указан, передаем None
    ext = args.ext if hasattr(args, 'ext') else None
    print(f"Pattern: {args.pattern}, Ext: {ext}")  # Отладочный вывод
    renamer_functions.rename_files(args.pattern, ext)


if __name__ == "__main__":
    main()
