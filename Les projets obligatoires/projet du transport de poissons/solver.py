# solver.py
import pyomo.environ as aml
from pyomo.opt import SolverFactory

def solve_fish_transport(data):
    num_locations = len(data["distance_matrix"])
    locations = list(range(num_locations))
    customers = list(range(1, num_locations))
    
    model = aml.ConcreteModel()
    
    # Ensembles
    model.V = aml.Set(initialize=locations)
    model.C = aml.Set(initialize=customers)
    model.K = aml.RangeSet(1, data["num_vehicles"])
    
    # Variables de décision
    model.x = aml.Var(model.V, model.V, model.K, domain=aml.Binary)
    model.u = aml.Var(model.V, model.K, domain=aml.NonNegativeReals)
    
    # Fonction Objectif: Minimiser la distance totale
    def objective_rule(model):
        return sum(data["distance_matrix"][i][j] * model.x[i, j, k] 
                   for i in model.V for j in model.V for k in model.K if i != j)
    model.obj = aml.Objective(rule=objective_rule, sense=aml.minimize)
    
    # Contraintes
    def visit_customer_rule(model, j):
        return sum(model.x[i, j, k] for i in model.V for k in model.K if i != j) == 1
    model.visit_customer = aml.Constraint(model.C, rule=visit_customer_rule)
    
    def flow_conservation_rule(model, h, k):
        return sum(model.x[i, h, k] for i in model.V if i != h) == sum(model.x[h, j, k] for j in model.V if j != h)
    model.flow_conservation = aml.Constraint(model.V, model.K, rule=flow_conservation_rule)
    
    def start_from_depot_rule(model, k):
        return sum(model.x[0, j, k] for j in model.C) <= 1
    model.start_from_depot = aml.Constraint(model.K, rule=start_from_depot_rule)
    
    M = 10000
    def capacity_subtour_rule(model, i, j, k):
        if i == j:
            return aml.Constraint.Skip
        return model.u[j, k] >= model.u[i, k] + data["demands"][j] - M * (1 - model.x[i, j, k])
    model.capacity_and_subtour = aml.Constraint(model.V, model.V, model.K, rule=capacity_subtour_rule)
    
    def capacity_limit_rule(model, i, k):
        return model.u[i, k] <= data["vehicle_capacity"]
    model.capacity_limit = aml.Constraint(model.V, model.K, rule=capacity_limit_rule)
    
    # Chemin vers le solveur GLPK
    chemin_executable = r"C:\glpk-5.0\w64\glpsol.exe"
    opt = SolverFactory('glpk', executable=chemin_executable)
    
    opt.solve(model)
    return model