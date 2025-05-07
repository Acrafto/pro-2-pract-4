# I'll use this archive to write all the code since the practice it self its vere short and I want to keep it simple
# I know that in a real project for a company, this code shold be very modular, but it is so short that I think dividing it 
# in multiple files would be counterproductive.
# Also in the pdf it says that we use objects and stuff, but I dont think it is necessary for this practice.

from materials.avl_tree import *

def read_patients(ruta_csv):
    """
    Lee un archivo CSV con datos de pacientes y los inserta en un árbol AVL.

    Args:
        ruta_csv (str): Ruta al archivo CSV que contiene los datos de los pacientes.

    Returns:
        AVL: Un árbol AVL con los datos de los pacientes, donde el DNI es la clave y el resto de los datos son el valor.
    """
    import csv
    tree = AVL()
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            dni = fila["DNI"]
            nombre = fila["Nombre"]
            sexo = fila["Sexo"]
            edad = fila["Edad"]

            diagnosticos = fila["Diagnosticos"].strip("[]").replace("'", "")
            diagnosticos = diagnosticos.split(", ") if diagnosticos else []
            
            alergias = fila["Alergias"].strip("[]").replace("'", "")
            alergias = alergias.split(", ") if alergias else []
            
            fecha_ultima_visita = fila["FechaUltimaVisita"]

            tree[dni] = {
                "Nombre": nombre,
                "Sexo": sexo,
                "Edad": edad,
                "Diagnosticos": diagnosticos,
                "Alergias": alergias,
                "FechaUltimaVisita": fecha_ultima_visita
            }
        return tree

def print_tree_hierarchy(tree, node=None, prefix="", is_left=True):
    """
    Imprime un árbol AVL en formato jerárquico con ramas visuales.

    Args:
        tree (AVL): El árbol AVL que se desea imprimir.
        node (Node, optional): Nodo desde el cual comenzar la impresión. Por defecto es la raíz.
        prefix (str, optional): Prefijo para alinear los nodos. Por defecto es una cadena vacía.
        is_left (bool, optional): Indica si el nodo actual es hijo izquierdo. Por defecto es True.
    """
    if node is None:
        node = tree.root()

    if node is not None:
        branch = "└── " if is_left else "┌── "
        print(f"{prefix}{branch}{node.key()}: {node.value()}")

        if tree.left(node) or tree.right(node):
            child_prefix = prefix + ("    " if is_left else "│   ")
            if tree.left(node):
                print_tree_hierarchy(tree, tree.left(node), child_prefix, True)
            if tree.right(node):
                print_tree_hierarchy(tree, tree.right(node), child_prefix, False)

def get_tree_keys(tree: AVL) -> list:
    """
    Obtiene todas las claves de un árbol AVL.

    Args:
        tree (AVL): El árbol AVL del cual se desean obtener las claves.

    Returns:
        list: Lista de claves presentes en el árbol.
    """
    return [key for key in tree]

def combined_base(tree1: AVL, tree2: AVL) -> AVL:
    """
    Fusiona dos árboles AVL en una base combinada, incluyendo todos los pacientes.

    Args:
        tree1 (AVL): Primer árbol AVL.
        tree2 (AVL): Segundo árbol AVL.

    Returns:
        AVL: Un nuevo árbol AVL que contiene todos los pacientes de ambos árboles.
    """
    combined_tree = AVL()
    shared_keys = set(tree1.keys()).intersection(set(tree2.keys()))
    keys1 = get_tree_keys(tree1)
    keys2 = get_tree_keys(tree2)
    shared_keys = list(set(keys1) & set(keys2))
    not_shared_keys1 = list(set(keys1) - set(shared_keys))
    not_shared_keys2 = list(set(keys2) - set(shared_keys))
    for key in not_shared_keys1:
        combined_tree[key] = tree1[key]
    for key in not_shared_keys2:
        combined_tree[key] = tree2[key]
    for key in shared_keys:
        if tree1[key]["FechaUltimaVisita"] > tree2[key]["FechaUltimaVisita"]:
            recent_data = tree1[key]
            older_data = tree2[key]
        else:
            recent_data = tree2[key]
            older_data = tree1[key]
        combined_tree[key] = {
            "Nombre": recent_data["Nombre"],
            "Sexo": recent_data["Sexo"],
            "Edad": recent_data["Edad"],
            "Diagnosticos": list(set(recent_data["Diagnosticos"] + older_data["Diagnosticos"])),
            "Alergias": list(set(recent_data["Alergias"] + older_data["Alergias"])),
            "FechaUltimaVisita": recent_data["FechaUltimaVisita"]
        }
    return combined_tree

def common_base(tree1: AVL, tree2: AVL) -> AVL:
    """
    Fusiona dos árboles AVL en una base común, incluyendo solo los pacientes compartidos.

    Args:
        tree1 (AVL): Primer árbol AVL.
        tree2 (AVL): Segundo árbol AVL.

    Returns:
        AVL: Un nuevo árbol AVL que contiene solo los pacientes compartidos entre ambos árboles.
    """
    common_base_tree = AVL()
    shared_keys = set(tree1.keys()).intersection(set(tree2.keys()))
    keys1 = get_tree_keys(tree1)
    keys2 = get_tree_keys(tree2)
    shared_keys = list(set(keys1) & set(keys2))
    for key in shared_keys:
        if tree1[key]["FechaUltimaVisita"] > tree2[key]["FechaUltimaVisita"]:
            recent_data = tree1[key]
            older_data = tree2[key]
        else:
            recent_data = tree2[key]
            older_data = tree1[key]
        common_base_tree[key] = {
            "Nombre": recent_data["Nombre"],
            "Sexo": recent_data["Sexo"],
            "Edad": recent_data["Edad"],
            "Diagnosticos": list(set(recent_data["Diagnosticos"] + older_data["Diagnosticos"])),
            "Alergias": list(set(recent_data["Alergias"] + older_data["Alergias"])),
            "FechaUltimaVisita": recent_data["FechaUltimaVisita"]
        }
    return common_base_tree

def menu():
    """
    Muestra un menú interactivo para realizar diferentes acciones con los árboles AVL.

    Opciones:
        1. Cargar datos de pacientes.
        2. Fusionar bases de datos (base combinada).
        3. Fusionar pacientes compartidos (base común).
        4. Salir del programa.
    """
    saludplus_tree = None
    vitalclinic_tree = None

    while True:
        print("Menú principal:")
        print("1. Cargar datos de pacientes")
        print("2. Fusionar bases de datos (base combinada)")
        print("3. Fusionar pacientes compartidos (base común)")
        print("4. Salir")

        opcion = input("Seleccione una opción insertando su número correspondiente: ")

        if opcion == "1":
            print("Cargando datos de SaludPlus...")
            saludplus_tree = read_patients("data/pacientes_saludplus.csv")
            print("Datos de SaludPlus cargados.")
            print_tree_hierarchy(saludplus_tree)

            print("\nCargando datos de VitalClinic...")
            vitalclinic_tree = read_patients("data/pacientes_vitalclinic.csv")
            print("Datos de VitalClinic cargados.")
            print_tree_hierarchy(vitalclinic_tree)
            print("\n--------------------")
            print("\nDatos correctamente cargados.")
            print("\n--------------------")
            
        elif opcion == "2":
            if saludplus_tree is None or vitalclinic_tree is None:
                print("Primero debe cargar los datos de los pacientes.")
            else:
                combined_tree = combined_base(saludplus_tree, vitalclinic_tree)
                print("Base combinada:")
                print_tree_hierarchy(combined_tree)

        elif opcion == "3":
            if saludplus_tree is None or vitalclinic_tree is None:
                print("Primero debe cargar los datos de los pacientes.")
            else:
                common_tree = common_base(saludplus_tree, vitalclinic_tree)
                print("Base común:")
                print_tree_hierarchy(common_tree)

        elif opcion == "4":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Asegúrese de seleccionar correctamente.")
    return None

if __name__ == "__main__":
    menu()




