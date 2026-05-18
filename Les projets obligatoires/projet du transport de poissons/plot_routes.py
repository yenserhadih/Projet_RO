# plot_routes.py
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as aml

def plot_optimized_routes(data, model):
    """
    Génère un graphique visuel des routes optimales pour le transport de poisson.
    """
    G = nx.DiGraph()
    
    # Définir des positions approximatives pour les sites (NDB, NKC et points de vente)
    # Le dépôt 0 est mis au centre, les autres autour
    pos = {
        0: (0, 0),    # Dépôt / Port Principal
        1: (-2, 3),   # Point 1
        2: (2, 4),    # Point 2
        3: (4, 1),    # Point 3
        4: (3, -3),   # Point 4
        5: (-1, -4),  # Point 5
        6: (-3, -1)   # Point 6
    }
    
    # Ajouter les nœuds (les sites)
    for node in pos:
        G.add_node(node)
        
    plt.figure(figsize=(10, 8))
    
    # Dessiner les nœuds (Le dépôt en rouge, les clients en bleu)
    nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='red', node_size=800, label='Port/Dépôt (0)')
    nx.draw_networkx_nodes(G, pos, nodelist=list(range(1, len(pos))), node_color='skyblue', node_size=600, label='Marchés/Clients')
    
    # Liste de couleurs pour distinguer les camions
    colors = ['green', 'blue', 'orange', 'purple']
    
    # Parcourir le modèle Pyomo pour extraire les arcs actifs (x[i,j,k] > 0.5)
    for k in model.K:
        edge_list = []
        color_idx = (k - 1) % len(colors)
        
        for i in model.V:
            for j in model.V:
                if aml.value(model.x[i, j, k]) > 0.5:
                    edge_list.append((i, j))
                    
        if edge_list:
            nx.draw_networkx_edges(
                G, pos, edgelist=edge_list, 
                edge_color=colors[color_idx], 
                width=2.5, arrows=True, arrowsize=20,
                label=f'Camion N° {k}'
            )
            
    # Ajouter les étiquettes des numéros de sites
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', font_weight='bold')
    
    plt.title("PROJET RO : Cartographie des Routes Optimales (Transport de Poisson)", fontsize=14, fontweight='bold')
    plt.legend(loc='upper left')
    plt.grid(False)
    plt.axis('off')
    
    print("[+] Génération de la carte graphique des routes...")
    plt.show()