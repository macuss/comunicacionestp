class ShannonFano:
    def _construir_codigos_recursivo(self, simbolos_freq, codigo_actual=""):
        """
        Función recursiva para construir los códigos Shannon-Fano.
        Args:
            simbolos_freq (list): Lista de tuplas (símbolo, frecuencia) ordenada descendentemente por frecuencia.
            codigo_actual (str): El prefijo de código actual.
        Returns:
            dict: La tabla de códigos Shannon-Fano.
        """
        if not simbolos_freq:
            return {}
        if len(simbolos_freq) == 1:
            return {simbolos_freq[0][0]: codigo_actual}

        # Encontrar el punto de división que minimiza la diferencia de frecuencias
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
                # Priorizar división más equilibrada, si hay empate en diff
                punto_division = i + 1

        grupo1 = simbolos_freq[:punto_division]
        grupo2 = simbolos_freq[punto_division:]

        codigos = {}
        codigos.update(self._construir_codigos_recursivo(grupo1, codigo_actual + "0"))
        codigos.update(self._construir_codigos_recursivo(grupo2, codigo_actual + "1"))
        return codigos

    def generar_codigos_shannon_fano(self, frecuencias):
        """
        Genera la tabla de códigos Shannon-Fano a partir de las frecuencias.
        Args:
            frecuencias (dict): Diccionario de frecuencias de caracteres.
        Returns:
            dict: La tabla de códigos Shannon-Fano.
        """
        # Ordenar símbolos por frecuencia de forma descendente
        simbolos_ordenados = sorted(frecuencias.items(), key=lambda item: item[1], reverse=True)
        return self._construir_codigos_recursivo(simbolos_ordenados)

    def codificar_shannon_fano(self, texto, codigos):
        """
        Codifica un texto usando la tabla de códigos Shannon-Fano.
        Args:
            texto (str): El texto a codificar.
            codigos (dict): La tabla de códigos Shannon-Fano.
        Returns:
            str: El texto codificado como una cadena de bits.
        """
        codificado = "".join(codigos.get(char, '') for char in texto)
        return codificado

    def decodificar_shannon_fano(self, bits_codificados, codigos):
        """
        Decodifica una secuencia de bits usando la tabla de códigos Shannon-Fano.
        Args:
            bits_codificados (str): La secuencia de bits a decodificar.
            codigos (dict): La tabla de códigos Shannon-Fano (necesita estar invertida para decodificar).
        Returns:
            str: El texto decodificado.
        """
        # Invertir el diccionario de códigos para una búsqueda eficiente
        codigos_inverso = {v: k for k, v in codigos.items()}
        decodificado = []
        buffer_bits = ""
        for bit in bits_codificados:
            buffer_bits += bit
            if buffer_bits in codigos_inverso:
                decodificado.append(codigos_inverso[buffer_bits])
                buffer_bits = "" # Resetear buffer para el siguiente carácter
        return "".join(decodificado)