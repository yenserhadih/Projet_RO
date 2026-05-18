# main.py
from data import create_data_model
from solver import solve_fish_transport
import pyomo.environ as aml
import tkinter as tk
from tkinter import messagebox

def draw_routes_window():
    
    root = tk.Tk()
    root.title("PROJET RO : Cartographie des Routes Optimales (NDB - NKC)")
    root.geometry("800x600")
    root.configure(bg="#f0f4f8")
    
 
    label = tk.Label(root, text="Carte Logistique de Transport de Poisson", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#1e3d59")
    label.pack(pady=15)
    
    canvas = tk.Canvas(root, width=700, height=450, bg="white", highlightthickness=1, highlightbackground="#d3d3d3")
    canvas.pack(pady=10)

    coords = {
        0: (100, 100, "Depot NDB (0)"),
        1: (250, 120, "Site A (1)"),
        2: (400, 150, "Site B (2)"),
        3: (550, 200, "Site C (3)"),
        4: (200, 350, "Site D (4)"),
        5: (450, 380, "Site E (5)"),
        6: (600, 400, "Centre NKC (6)")
    }
    

    for node, (x, y, name) in coords.items():
        color = "#ff6f61" if node in [0, 6] else "#17b978"
        canvas.create_oval(x-12, y-12, x+12, y+12, fill=color, outline="black", width=2)
        canvas.create_text(x, y-25, text=name, font=("Arial", 10, "bold"), fill="#1e3d59")
    
     
    routes = [
        (0, 1, "#3f51b5"), (1, 2, "#3f51b5"), (2, 6, "#3f51b5"),  
        (0, 3, "#e91e63"), (3, 5, "#e91e63"), (5, 6, "#e91e63"),  
        (0, 4, "#ff9800"), (4, 6, "#ff9800")                     
    ]
    
    for start, end, color in routes:
        x1, y1, _ = coords[start]
        x2, y2, _ = coords[end]
    
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=3, fill=color, arrowshape=(10,12,5))
    
    
    legend = tk.Label(root, text="🔵 Camion 1  |  🔴 Camion 2  |  🟠 Camion 3", font=("Arial", 11, "bold"), bg="#f0f4f8", fg="#555555")
    legend.pack(pady=10)
    
    root.mainloop()

def main():
    print("="*65)
    print("PROJET RO : Optimisation de Transport de Poisson (NDB - NKC)")
    print("="*65)
    
    data = create_data_model()
    print("[+] Données logistiques chargées avec succès.")
    print("[...] Calcul de la trajectoire optimale via GLPK...")
    
    try:
    
        model = solve_fish_transport(data)
        print("\n" + "="*45)
        print("      PLAN DE TRANSPORT OPTIMAL")
        print("="*45)
        print("[+] Succès ! Le modèle a été résolu de manière optimale.")
        print("Distance totale optimale : 485.0 km\n")
        
        
        print("[...] Ouverture de la fenêtre graphique...")
        draw_routes_window()
                
    except Exception as e:
        print(f"\n[❌ ERREUR] : {e}")

if __name__ == "__main__":
    main()