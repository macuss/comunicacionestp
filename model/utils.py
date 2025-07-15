import collections

class Utils:
    def calcular_frecuencias(self, texto):
        return collections.Counter(texto)

    def calcular_longitud_promedio(self, frecuencias, codigos):
        total_bits = sum(frecuencias[char] * len(codigos[char]) for char in frecuencias if char in codigos)
        total_caracteres = sum(frecuencias.values())
        return total_bits / total_caracteres if total_caracteres > 0 else 0

    def calcular_tasa_compresion(self, texto_original, texto_codificado_bits):
        if not texto_original:
            return 0.0

        # Tamaño en bits del texto original (considerando 8 bits por carácter ASCII/UTF-8 simple)
        tamano_original_bits = len(texto_original) * 8
        tamano_codificado_bits = len(texto_codificado_bits)

        if tamano_original_bits == 0:
            return 0.0

        return (1 - (tamano_codificado_bits / tamano_original_bits)) * 100