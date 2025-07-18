class ShannonFano:
    def _construir_codigos_recursivo(self, simbolos_freq, codigo_actual=""):

        if not simbolos_freq:
            return {}
        if len(simbolos_freq) == 1:
            return {simbolos_freq[0][0]: codigo_actual}


        total_freq = sum(freq for _, freq in simbolos_freq)
        acumulado = 0
        punto_division = 0
        min_diff = float('inf')

        for i in range(len(simbolos_freq) - 1):
            acumulado += simbolos_freq[i][1]
            diff = abs(total_freq - 2 * acumulado)
            if diff < min_diff:
                min_diff = diff
                punto_division = i + 1
            elif diff == min_diff and abs(total_freq - 2 * (acumulado - simbolos_freq[i][1])) < diff:

                punto_division = i + 1

        grupo1 = simbolos_freq[:punto_division]
        grupo2 = simbolos_freq[punto_division:]

        codigos = {}
        codigos.update(self._construir_codigos_recursivo(grupo1, codigo_actual + "0"))
        codigos.update(self._construir_codigos_recursivo(grupo2, codigo_actual + "1"))
        return codigos

    def generar_codigos_shannon_fano(self, frecuencias):

        simbolos_ordenados = sorted(frecuencias.items(), key=lambda item: item[1], reverse=True)
        return self._construir_codigos_recursivo(simbolos_ordenados)

    @staticmethod
    def codificar_shannon_fano(texto, codigos):

        codificado = "".join(codigos.get(char, '') for char in texto)
        return codificado

    @staticmethod
    def decodificar_shannon_fano(bits_codificados, codigos):

        # invierte el dicc de códigos para una búsqueda eficiente
        codigos_inverso = {v: k for k, v in codigos.items()}
        decodificado = []
        buffer_bits = ""
        for bit in bits_codificados:
            buffer_bits += bit
            if buffer_bits in codigos_inverso:
                decodificado.append(codigos_inverso[buffer_bits])
                buffer_bits = ""
        return "".join(decodificado)