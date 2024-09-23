import networkx as nx
import matplotlib.pyplot as plt
import re

# Función para leer la gramática desde un archivo
def read_grammar_from_file(filename):
    grammar_patterns = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Ignorar líneas vacías y comentarios
            left, right = line.split("->")
            left = left.strip()
            right = right.strip()
            grammar_patterns[left] = right
    return grammar_patterns

# Función para construir expresiones regulares de la gramática
def build_regex(grammar):
    regex_patterns = {}
    for non_terminal, production in grammar.items():
        if non_terminal == 'S':
            regex_patterns[non_terminal] = f'^{grammar["A"]}{grammar["B"]}$'
        else:
            regex_patterns[non_terminal] = production.strip()
    return regex_patterns

# Función para verificar si una cadena es válida según la gramática
def is_valid_string(regex_patterns, string):
    return re.match(regex_patterns['S'], string) is not None

# Función para construir el árbol de derivación
def build_derivation_tree(G, parent, string):
    if not string:
        return

    # Dividir la cadena en partes A y B
    A_part = re.match(regex_patterns['A'], string).group(0)
    B_part = re.match(regex_patterns['B'], string[len(A_part):]).group(0)

    # Crear nodos para cada símbolo terminal
    G.add_edge(parent, 'S')  # Nodo raíz

    # Añadir nodos solo para cada símbolo en A y B
    for char in A_part:
        G.add_edge('S', f'{char}')  # Solo el símbolo terminal
    for char in B_part:
        G.add_edge('S', f'{char}')  # Solo el símbolo terminal

# Leer la gramática desde el archivo
grammar_file = 'gramatica.txt'
grammar = read_grammar_from_file(grammar_file)
regex_patterns = build_regex(grammar)

# Pedir al usuario ingresar una cadena de prueba
test_string = input("Ingresa una cadena para validar: ")

# Verificar si la cadena es válida según la gramática
if is_valid_string(regex_patterns, test_string):
    print(f"Cadena válida: {test_string}")
    
    # Construir el árbol de derivación para la cadena válida
    G = nx.DiGraph()
    build_derivation_tree(G, 'S', test_string)

    # Dibuja el árbol con mejoras visuales
    pos = nx.spring_layout(G)  # Cambia la disposición si lo deseas
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000, font_color='black', font_weight='bold', edge_color='gray', arrows=True)
    plt.title(f"Árbol de Derivación para: {test_string}", fontsize=14)
    plt.savefig(f"arbol_derivacion_{test_string}.png")
    # plt.show()  # Comentar esta línea si no hay soporte gráfico

    print(f"El árbol de derivación se ha guardado como 'arbol_derivacion_{test_string}.png'")
else:
    print(f"Cadena inválida: {test_string}")

