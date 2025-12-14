#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тесты для модуля renamer_functions.py с использованием pytest
"""
import os
import shutil
import sys
import pytest

# Добавление пути к модулю renamer_functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from renamer_functions import (
    is_safe_directory,
    get_file_extension,
    should_rename_file,
    generate_new_filename,
    rename_files
)


@pytest.fixture
def test_dir(tmp_path):
    """Создает временную директорию с тестовыми файлами."""
    test_files = [
        'file1.txt',
        'file2.txt',
        'file3.csv',
        'file4.png',
        'file5',  # файл без расширения
    ]
    
    for filename in test_files:
        (tmp_path / filename).touch()
    
    return tmp_path


def test_is_safe_directory(monkeypatch):
    """Тест функции is_safe_directory."""
    # Текущая директория должна быть безопасной
    assert is_safe_directory()
    
    # Системные директории должны быть небезопасными
    unsafe_dirs = ["/", "/root", "/home", "/etc", "/bin", "/usr", "/var"]
    for unsafe_dir in unsafe_dirs:
        monkeypatch.setattr(os, 'getcwd', lambda: unsafe_dir)
        assert not is_safe_directory()


def test_get_file_extension():
    """Тест функции get_file_extension."""
    assert get_file_extension('file.txt') == 'txt'
    assert get_file_extension('file.tar.gz') == 'gz'
    assert get_file_extension('file') == ''
    assert get_file_extension('file.') == ''
    assert get_file_extension('.hidden') == 'hidden'


def test_should_rename_file():
    """Тест функции should_rename_file."""
    # Если ext не указан, переименовываются все файлы
    assert should_rename_file('file.txt', None)
    assert should_rename_file('file', None)
    
    # Если ext указан, переименовываются только файлы с указанными расширениями
    assert should_rename_file('file.txt', ['.txt'])
    assert not should_rename_file('file.csv', ['.txt'])
    assert should_rename_file('file.csv', ['.txt', '.csv'])
    
    # Файлы без расширения не переименовываются, если ext указан
    assert not should_rename_file('file', ['.txt'])


def test_generate_new_filename():
    """Тест функции generate_new_filename."""
    # Файлы с расширением
    assert generate_new_filename('file.txt', 'newfile', 1) == 'newfile_1.txt'
    assert generate_new_filename('file.csv', 'newfile', 2) == 'newfile_2.csv'
    
    # Файлы без расширения
    assert generate_new_filename('file', 'newfile', 3) == 'newfile_3'


def test_rename_files_all_files(test_dir):
    """Тест функции rename_files для переименования всех файлов."""
    os.chdir(test_dir)
    rename_files('newfile', None)
    
    # Проверяем, что все файлы переименованы
    expected_files = {
        'newfile_1.txt',
        'newfile_2.txt',
        'newfile_3.csv',
        'newfile_4.png',
        'newfile_5',
    }
    
    actual_files = set(os.listdir(test_dir))
    assert expected_files == actual_files


def test_rename_files_specific_extensions(test_dir):
    """Тест функции rename_files для переименования файлов с указанными расширениями."""
    os.chdir(test_dir)
    rename_files('txtfile', ['.txt'])
    
    # Проверяем, что только файлы с расширением .txt переименованы
    expected_files = {
        'txtfile_1.txt',
        'txtfile_2.txt',
        'file3.csv',
        'file4.png',
        'file5',
    }
    
    actual_files = set(os.listdir(test_dir))
    assert expected_files == actual_files


def test_rename_files_multiple_extensions(test_dir):
    """Тест функции rename_files для переименования файлов с несколькими расширениями."""
    os.chdir(test_dir)
    rename_files('datfile', ['.csv', '.png'])
    
    # Проверяем, что только файлы с расширениями .csv и .png переименованы
    expected_files = {
        'file1.txt',
        'file2.txt',
        'datfile_1.csv',
        'datfile_2.png',
        'file5',
    }
    
    actual_files = set(os.listdir(test_dir))
    assert expected_files == actual_files


def test_rename_files_unsafe_directory(test_dir, monkeypatch, capsys):
    """Тест функции rename_files для проверки безопасности директории."""
    monkeypatch.setattr(os, 'getcwd', lambda: "/")
    os.chdir(test_dir)
    
    # Функция должна вывести сообщение об ошибке и не переименовывать файлы
    rename_files('newfile', None)
    
    # Проверяем, что файлы не были переименованы
    original_files = {
        'file1.txt',
        'file2.txt',
        'file3.csv',
        'file4.png',
        'file5',
    }
    
    actual_files = set(os.listdir(test_dir))
    assert original_files == actual_files
    
    # Проверяем, что сообщение об ошибке было выведено
    captured = capsys.readouterr()
    assert "Ошибка: Выполнение в системной директории запрещено." in captured.out
