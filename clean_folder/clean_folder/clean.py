import sys
import os
import re
import patoolib
from shutil import move as shutil_move

FILES_FORMAT = {'images': ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP'),
                'files': ('AVI', 'MP4', 'MOV', 'MKV'),
                'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                'music': ('MP3', 'OGG', 'WAV', 'AMR'),
                'archives': ('ZIP', 'GZ', 'TAR', 'RAR', '7Z')
                }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

DICTIONARY_FOR_TRANSLITERATION = {}

for cyr, tran in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    DICTIONARY_FOR_TRANSLITERATION[ord(cyr)] = tran
    DICTIONARY_FOR_TRANSLITERATION[ord(cyr.upper())] = tran.upper()
    
know_extentions = set()
unknow_extentions = set()

sorted_files = {'images': [],
                'files': [],
                'documents': [],
                'music': [],
                'archives': [],
                'unknown_extensions': []
                }
    
    
def normalize(name):
    file_name, file_extention = os.path.splitext(name)
    translated_name = ''
    pattern = r'[a-zA-Z0-9]'
    for symbol in file_name:
        if re.search(pattern, symbol) != None:
            translated_name += symbol
        elif ord(symbol) in DICTIONARY_FOR_TRANSLITERATION:
            translated_name += DICTIONARY_FOR_TRANSLITERATION[ord(symbol)]
        else:
            translated_name += '_'

    return translated_name + file_extention


def move_file(file, file_path):
    normalized_file_name = normalize(file)
    file_name, file_extention = os.path.splitext(normalized_file_name)
    file_format_sorting(normalized_file_name, file)
    for key, value in FILES_FORMAT.items():
        new_path = f'{PATH}\\{key}'
        if normalized_file_name.upper().endswith(value):
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            if key == 'archives':
                patoolib.extract_archive(
                    file_path, outdir=f'{new_path}\\{file_name}')
                os.remove(file_path)
            else:
                shutil_move(file_path, f'{new_path}\\{normalized_file_name}')
        elif not normalized_file_name.upper().endswith(value):
            unknow_extentions.add(file_extention)

    # unknown_extensions_path = f'{PATH}\\unknown_extensions'
    # if not os.path.exists(unknown_extensions_path):
    #     os.makedirs(unknown_extensions_path)
    # shutil_move(
    #     file_path, f'{unknown_extensions_path}\\{normalized_file_name}')


def file_format_sorting(file, origin_file_name):
    for key, value in FILES_FORMAT.items():
        if file.upper().endswith(value):
            sorted_files[key].append(file)
            return
    sorted_files['unknown_extensions'].append(origin_file_name)
    return


def remove_empty_directory(path):
    sys.setrecursionlimit(10000)
    for file in os.scandir(path):
        if file.name not in sorted_files.keys() and file.is_dir():
            if not any(os.scandir(file.path)):
                os.rmdir(file.path)
            elif any(os.scandir(file.path)):
                remove_empty_directory(file.path)
            return remove_empty_directory(path)


def tree_directory(path):
    for file in os.scandir(path):
        if file.is_dir() and file.name not in sorted_files.keys():
            tree_directory(file.path)
        elif file.name in sorted_files.keys():
            continue
        else:
            move_file(file.name, file.path)


def get_path():
    if len(sys.argv) == 2:
        file, path = sys.argv
        return path
    else:
        flag_error = '****ERROR****\nThe program work with only parameter path.\nFor example: main.py /path/to/directiry\nTry run again'
        print(flag_error)

def start():
    global PATH
    PATH = get_path()
    tree_directory(PATH)
    remove_empty_directory(PATH)


if __name__ == '__main__':
    for cyr, tran in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        DICTIONARY_FOR_TRANSLITERATION[ord(cyr)] = tran
        DICTIONARY_FOR_TRANSLITERATION[ord(cyr.upper())] = tran.upper()

    sorted_files = {'images': [],
                    'files': [],
                    'documents': [],
                    'music': [],
                    'archives': [],
                    'unknown_extensions': []
                    }
    PATH = get_path()
    know_extentions = set()
    unknow_extentions = set()

    if PATH != None:
        tree_directory(PATH)
        remove_empty_directory(PATH)
        print(know_extentions)
        print(unknow_extentions)