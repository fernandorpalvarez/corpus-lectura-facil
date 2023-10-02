import pandas as pd


if __name__ == '__main__':
    path = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/corpus_lenguaje_natural/infolibros_es.txt"
    df = pd.read_csv(path, delimiter='\t')