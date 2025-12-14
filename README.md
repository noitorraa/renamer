# RenamerApp

Простая утилита для массового переименования файлов в директории.

## Как использовать

### 1. Переименовать все файлы
```bash
python main.py --pattern newfile
```
Пример:
- `file1.txt` → `newfile_1.txt`
- `image.png` → `newfile_2.png`

### 2. Переименовать только определенные файлы
```bash
python main.py --pattern doc --extension .txt .pdf
```
Пример:
- `file1.txt` → `doc_1.txt`
- `file2.pdf` → `doc_2.pdf`
- `image.png` остается без изменений

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd RenamerApp
   ```

2. Создайте виртуальное окружение (опционально):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```

3. Установите зависимости для тестов:
   ```bash
   pip install -r requirements.txt
   ```

## Тестирование

Запустите тесты:
```bash
pytest tests/
```

## Безопасность

Скрипт не будет работать в системных директориях (`/`, `/etc`, `/root` и т.д.).
