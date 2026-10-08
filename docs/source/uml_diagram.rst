UML Диаграмма отношения классов в программе
===========================================

.. mermaid::


   classDiagram
    
    class Seq {
        # NUCLEOTIDE_BASES: set
        # PROTEIN_AMINOACIDS: set
        - header: str
        - sequence: str
        + \_\_str__() str
        + \_\_len__() int
        + alphabet() str
    }

    class FastaReader {
        - file_path: str
        + is_valid_fasta() bool
        + \_\_iter__() Iterator[Seq]
    }
    
    FastaReader ..> Seq
