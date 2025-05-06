#I'll use this archive to write all the code since the practice it self its vere short and I want to keep it simple, but if gets messy
# I will split it into different files. 
from materials.avl_tree import *
def read_patients(ruta_csv):
    import csv
    tree= AVL() 
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:           
            dni=fila["DNI"]
            nombre=fila["Nombre"]
            sexo=fila["Sexo"]
            edad=fila["Edad"]

            diagnosticos = fila["Diagnosticos"].strip("[]").replace("'", "")
            diagnosticos = diagnosticos.split(", ") if diagnosticos else []
            
            alergias = fila["Alergias"].strip("[]").replace("'", "")
            alergias = alergias.split(", ") if alergias else []
            
            fecha_ultima_visita=fila["FechaUltimaVisita"]

            tree[dni]={
                "Nombre": nombre,
                "Sexo": sexo,
                "Edad": edad,
                "Diagnosticos": diagnosticos,
                "Alergias": alergias,
                "FechaUltimaVisita": fecha_ultima_visita
            }
        return tree

#Cool function I found somewhere and adapted a bit here to print the tree in a more readable way.
def print_tree_hierarchy(tree, node=None, prefix=""):
    if node is None:
        node = tree.root()  

    if node is not None:
        print(f"{prefix}└── {node.key()}: {node.value()}")  
        left_child = tree.left(node)  
        right_child = tree.right(node)  
        if left_child is not None:
            print_tree_hierarchy(tree, left_child, prefix + "    ")
        if right_child is not None:
            print_tree_hierarchy(tree, right_child, prefix + "    ")  
      
    
if __name__ == "__main__":
    saludplus=read_patients("data/pacientes_saludplus.csv")
    print_tree_hierarchy(saludplus)
    vitalclinic=read_patients("data/pacientes_vitalclinic.csv") 
    print_tree_hierarchy(vitalclinic)

    
   

