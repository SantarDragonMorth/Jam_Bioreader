"""
Модуль для работы с биологическими последовательностями в формате FASTA.

Содержит два класса:
- Seq: для представления отдельной последовательности в FASTA формате
- FastaReader: для чтения и обработки FASTA файлов

Пример использования:
    >>> reader = FastaReader("sequences.fasta")
    >>> for seq in reader:
    ...     print(f"Заголовок: {seq.header}")
    ...     print(f"Длина: {len(seq)}")
    ...     print(f"Тип: {seq.alphabet()}")
"""

class Seq:
    """
    Этот класс предназначен для представления и работы с биологической последовательностью в формате FASTA.
    
    Он хранит в себе fasta-заголовок последовательности и саму последовательность, предоставляет методы для определения
    типа последовательности (Nucleotide, Protein) и работы с её данными.

    **Свойства класса:**

    Attributes:
        - header (str): Полный заголовок последовательности (без символа '>')
        - sequence (str): Биологическая последовательность в верхнем регистре
        
    Пример:
        >>> seq = Seq("seq1 Нуклеотидная последовательность", "ATCGATCG")
        >>> print(seq.header)
        seq1 Нуклеотидная последовательность
        >>> len(seq)
        8
        >>> seq.alphabet()
        "Nucleotide"
    
    Определение алфавитов для различных типов последовательностей:
    """
    
    _NUCLEOTIDE_BASES = set("ATCGUNatcgun")
    """Множество символов нуклеотидного алфавита (стандартные азотистые основания)"""
    
    _PROTEIN_AMINOACIDS = set("ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy*")
    """Множество символов белкового алфавита (стандартные аминокислоты и стоп-кодон)

    
    ­­
    **Методы класса:**"""

    # Конструктор класса (свойства: заголовок и последовтаельность)
    def __init__(self, header, sequence):
        """
        Создаёт объект последовательности.
        
        Args:
            header (str): Заголовок FASTA записи (вся строка после символа '>')
            sequence (str): Биологическая последовательность
            
        ПРЕОБРАЗОВАНИЯ:
            - Заголовок очищается от пробелов по краям
            - Последовательность очищается от пробелов и переводов строк, приводится к верхнему регистру
        """

        self.__header = header.strip()
        self.__sequence = "".join(sequence.split()).upper()
    
    # Доступ к заголовку
    @property
    def header(self):
        return self.__header
    
    # Доступ к последовательности
    @property
    def sequence(self):
        return self.__sequence

    # Приведение класса к строковому типу
    def __str__(self):
        """
        Возвращает строковое представление последовательности в формате FASTA.
        
        Returns:
            str: Последовательность в формате FASTA, записанная по 60 символов в строке
            
        Пример:
            >>> seq = Seq("test", "ATCG" * 20)
            >>> print(seq)  # Выведет последовательность в FASTA формате
        """
        
        # Форматирование последовательности с переносами каждые 60 символов
        lines = [f">{self.__header}"]
        for i in range(0, len(self.__sequence), 60):
            lines.append(self.__sequence[i:i+60])
        return "\n".join(lines)
    
    # Длина последовательности
    def __len__(self):
        """
        Возвращает длину последовательности.
        
        Returns:
            int: Количество символов в последовательности

        Пример:
            >>> seq = Seq("test", "ATCG" * 20)
            >>> print(len(seq))
            80
        """
        return len(self.__sequence)
    
    # Алфавит последовательности
    def alphabet(self):
        """
        Возвращает тип алфавита последовательности.
        
        Проверяет последовательность на принадлежность к одному из алфавитов:
        *Nucleotide* или *Protein*. Проверка выполняется в порядке приоритета.
        
        Returns:
            str: "Nucleotide", "Protein" или "Unknown"
            
        Пример:
            >>> seq = Seq("test", "ATCGATCG")
            >>> seq.alphabet()
            "Nucleotide"
        """

        seq_set = set(self.__sequence)
        
        # Проверка на нуклеотидную последовательность (содержит только A, T, C, G и дополнительные символы)
        if seq_set.issubset(self._NUCLEOTIDE_BASES):
            return "Nucleotide"
        
        # Проверка на белковую последовтаельность (содержит аминокислоты, записанные одной буквой)
        if seq_set.issubset(self._PROTEIN_AMINOACIDS):
            return "Protein"
        
        return "Unknown"
    
class FastaReader:
    """
    Этот класс предназначен для чтения и обработки FASTA файлов, содержащих биологические последовательности.
    
    Он обеспечивает чтение больших FASTA файлов с использованием генератора,
    проверку файлов на соответствие формату FASTA и последовательное извлечение записей (последовательностей), 
    т.е. отдельных экземпляров класса Seq.
    
    **Свойства класса:**

    Attributes:
        file_path (str): Путь к FASTA файлу
        
    Пример:
        >>> reader = FastaReader("sequences.fasta")
        >>> if reader.is_valid_fasta():
        ...     for seq in reader:
        ...         # Обработка каждой последовательности

    **Методы класса:**"""

    # Конструктор класса (свойство: путь к файлу)
    def __init__(self, file_path):
        """
        Создаёт ридер FASTA файлов.
        
        Args:
            file_path (str): Путь к FASTA файлу для чтения
        """
        self.__file_path = file_path
    
    # Доступ к пути
    @property
    def file_path(self):
        return self.__file_path

    # Проверка файла
    def is_valid_fasta(self):
        """
        Проверяет, соответствует ли файл формату FASTA.
        
        Проверка выполняется по первому символу файла - он должен быть '>'.
        
        Returns:
            bool: True если файл соответствует формату FASTA, False в случае ошибок или несоответствия формату
            
        Пример:
            >>> reader = FastaReader("sequences.fasta")
            >>> reader.is_valid_fasta()
            True
        """

        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                first_line = file.readline().strip()
                return first_line.startswith('>')
        except (IOError, UnicodeDecodeError):
            return False
    
    # Чтение файла и извлечение последовательностей
    def __iter__(self):
        """
        Генератор (итератор) для чтения записей из FASTA файла.
        
        Он читает файл построчно, собирает заголовки и последовательности,
        возвращая экземпляры Seq по мере чтения файла.
        
        Yields:
            Seq: Экземпляры последовательностей
            
        Raises:
            ValueError: Если файл не соответствует формату FASTA
            
        Пример:
            >>> reader = FastaReader("sequences.fasta")
            >>> for seq in reader:
            ...     print(seq.header)
        """
        if not self.is_valid_fasta():
            raise ValueError("Файл не соответствует формату FASTA")
        
        # Инициализация переменных для чтения файла
        header = None
        sequence_lines = []

        # Чтение файла построчно
        with open(self.__file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                
                if line.startswith('>'):
                    # Если есть последовательность, возвращаем её
                    if header is not None:
                        yield Seq(header, "".join(sequence_lines))
                    header = line[1:].strip()  # Убираем '>' в начале заголовка
                    sequence_lines = []

                elif line and header is not None:
                    # Добавление строки последовательности в список строк 
                    sequence_lines.append(line)
            
            # Возвращение последней последовательности
            if header is not None:
                yield Seq(header, "".join(sequence_lines))