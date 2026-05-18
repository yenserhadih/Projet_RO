# data.py

def create_data_model():
    data = {}
    
    # Matrice des distances en km
    data["distance_matrix"] = [
        [0, 10, 15, 20, 25, 18, 22],
        [10, 0, 8, 12, 17, 14, 16],
        [15, 8, 0, 10, 13, 11, 15],
        [20, 12, 10, 0, 9, 7, 12],
        [25, 17, 13, 9, 0, 6, 8],
        [18, 14, 11, 7, 6, 0, 5],
        [22, 16, 15, 12, 8, 5, 0]
    ]
    
    # Demandes des clients en kg
    data["demands"] = {0: 0, 1: 200, 2: 300, 3: 250, 4: 150, 5: 200, 6: 100}
    
    # Flotte de camions
    data["num_vehicles"] = 3
    data["vehicle_capacity"] = 700
    
    return data