import heapq
import pydot
import os


class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # Permite comparar nodos en el heapq basado en la frecuencia
    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    def construir_arbol_huffman(self, frecuencias):
        priority_queue = []
        for char, freq in frecuencias.items():
            heapq.heappush(priority_queue, HuffmanNode(char, freq))

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged_node = HuffmanNode(None, left.freq + right.freq, left, right)
            heapq.heappush(priority_queue, merged_node)

        return priority_queue[0] if priority_queue else None

    def generar_codigos_huffman(self, arbol, codigo_actual="", codigos={}):
        """
        Genera la tabla de códigos Huffman recursivamente.
        Args:
            arbol (HuffmanNode): El nodo actual del árbol.
            codigo_actual (str): El código binario construido hasta el momento.
            codigos (dict): Diccionario para almacenar los códigos generados.
        Returns:
            dict: La tabla de códigos Huffman.
        """
        if arbol is None:
            return

        # Si es un nodo hoja (tiene un carácter), es un código completo
        if arbol.char is not None:
            codigos[arbol.char] = codigo_actual if codigo_actual else '0'  # Caso de un solo caracter
            return

        # Recorrer hacia la izquierda (0) y la derecha (1)
        self.generar_codigos_huffman(arbol.left, codigo_actual + "0", codigos)
        self.generar_codigos_huffman(arbol.right, codigo_actual + "1", codigos)
        return codigos

    def codificar_huffman(self, texto, codigos):
        codificado = "".join(codigos.get(char, '') for char in texto)
        return codificado

    def decodificar_huffman(self, bits_codificados, arbol):
        decodificado = []
        nodo_actual = arbol
        for bit in bits_codificados:
            if bit == '0':
                nodo_actual = nodo_actual.left
            else:  # bit == '1'
                nodo_actual = nodo_actual.right

            if nodo_actual.char is not None:  # Si llegamos a un nodo hoja
                decodificado.append(nodo_actual.char)
                nodo_actual = arbol  # Resetear al inicio del árbol para el siguiente carácter
        return "".join(decodificado)

    def generar_arbol_graphviz(self, arbol, output_path="temp_huffman_tree.png"):
        """
        Genera una visualización del árbol de Huffman usando Graphviz.
        Args:
            arbol (HuffmanNode): La raíz del árbol de Huffman.
            output_path (str): Ruta donde se guardará la imagen del árbol.
        Returns:
            str: La ruta del archivo de imagen generado, o None si falla.
        """
        if not arbol:
            return None

        graph = pydot.Dot("huffman_tree", graph_type="digraph")
        nodes_created = {}  # Para evitar duplicados

        def add_nodes_edges(node):
            if node is None:
                return

            node_id = str(id(node))
            if node_id not in nodes_created:
                label = f"{node.char}:{node.freq}" if node.char is not None else f"{node.freq}"
                graph_node = pydot.Node(node_id, label=label, shape="circle")
                graph.add_node(graph_node)
                nodes_created[node_id] = graph_node

            if node.left:
                left_id = str(id(node.left))
                if left_id not in nodes_created:
                    label = f"{node.left.char}:{node.left.freq}" if node.left.char is not None else f"{node.left.freq}"
                    graph_node = pydot.Node(left_id, label=label, shape="circle")
                    graph.add_node(graph_node)
                    nodes_created[left_id] = graph_node
                graph.add_edge(pydot.Edge(nodes_created[node_id], nodes_created[left_id], label="0"))
                add_nodes_edges(node.left)

            if node.right:
                right_id = str(id(node.right))
                if right_id not in nodes_created:
                    label = f"{node.right.char}:{node.right.freq}" if node.right.char is not None else f"{node.right.freq}"
                    graph_node = pydot.Node(right_id, label=label, shape="circle")
                    graph.add_node(graph_node)
                    nodes_created[right_id] = graph_node
                graph.add_edge(pydot.Edge(nodes_created[node_id], nodes_created[right_id], label="1"))
                add_nodes_edges(node.right)

        add_nodes_edges(arbol)

        try:
            # que el directorio de salida exista, ver si funciona
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            graph.write_png(output_path)
            return output_path
        except Exception as e:
            print(f"Error al generar el árbol Graphviz: {e}")
            return None