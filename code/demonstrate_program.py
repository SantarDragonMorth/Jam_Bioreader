# Импорт классов для работы с FASTA файлами
from jam_bioreader import Seq, FastaReader

def demonstrate_classes():
    """
    Запрашивает у пользователя путь к FASTA файлу, проверяет его корректность и выводит подробную информацию о всех последовательностях в нём.
    
    **Программа выводит для каждой последовательности:**
        - Заголовок
        - Длину
        - Тип алфавита (нуклеотидный, белковый)
        - Первые 60 символов последовательности
        
    **Пример использования программы:**
        >>> demonstrate_classes()
        Введите путь к FASTA файлу: sequences.fasta
        Анализ файла: sequences.fasta
        ============================================================
        <BLANKLINE>
        Последовательность #1:
          Заголовок: seq1 Нуклеотидная последовательность
          Длина: 120
          Тип: Nucleotide
          Начало: ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG 
        <BLANKLINE> 
        ============================================================
    """
    # Ввод пути к FASTA файлу с клавиатуры
    file_path = input("Введите путь к FASTA файлу: ")
    
    # Создание ридера
    reader = FastaReader(file_path)
    
    # Проверка файла на соответсвие FASTA формату
    if not reader.is_valid_fasta():
        print(f"Ошибка: файл {file_path} не является FASTA файлом")
        return
    
    # Анализ последовательностей в файле
    print(f"Анализ файла: {file_path}")
    print("=" * 80)
    
    for i, seq in enumerate(reader, 1):
        print(f"\nПоследовательность #{i}:")
        print(f"  Заголовок: {seq.header}")
        print(f"  Длина: {len(seq)}")
        print(f"  Тип: {seq.alphabet()}")
        print(f"  Начало: {seq.sequence[:60]}")
    
    print("\n" + "=" * 80)

# Запуск программы
if __name__ == "__main__":
    """
    Основная точка входа в программу.
    
    При прямом запуске скрипта вызывает интерактивную функцию анализа FASTA файлов.
    """
    demonstrate_classes()