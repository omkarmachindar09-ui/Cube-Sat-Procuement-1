# Assembly start week
assembly_start_week = 16

# Define the toy Bill of Materials
bom = {
    "Solar Panel": {
        "required_qty": 4,
        "suppliers": {
            "A": {"cost": 5000, "lead_time": 8, "moq": 2},
            "B": {"cost": 5500, "lead_time": 5, "moq": 4}
        }
    },
    "Battery Pack": {
        "required_qty": 1,
        "suppliers": {
            "A": {"cost": 12000, "lead_time": 10, "moq": 1},
            "B": {"cost": 11000, "lead_time": 14, "moq": 1}
        }
    },
    "Reaction Wheel": {
        "required_qty": 3,
        "suppliers": {
            "A": {"cost": 8000, "lead_time": 8, "moq": 4},
            "B": {"cost": 8000, "lead_time": 6, "moq": 4}
        }
    },
    "Onboard Computer": {
        "required_qty": 1,
        "suppliers": {
            "A": {"cost": 15000, "lead_time": 7, "moq": 1},
            "B": {"cost": 14000, "lead_time": 13, "moq": 1}
        }
    }
}
import pulp

# Create the optimization model
model = pulp.LpProblem("CubeSat_Procurement", pulp.LpMinimize)

# Dictionary to store decision variables
x = {}

# Create decision variables for each supplier of each component
for component in bom:
    for supplier in bom[component]["suppliers"]:
        var_name = f"{component}_{supplier}"
        x[(component, supplier)] = pulp.LpVariable(var_name, lowBound=0, cat='Integer')

# Objective: minimize total cost
model += pulp.lpSum(
    bom[c]["suppliers"][s]["cost"] * x[(c, s)]
    for c in bom
    for s in bom[c]["suppliers"]
)

# Constraint 1: meet required quantity
for component in bom:
    model += pulp.lpSum(x[(component, s)] for s in bom[component]["suppliers"]) >= bom[component]["required_qty"]

# Constraint 2: lead time must be feasible
for component in bom:
    for supplier in bom[component]["suppliers"]:
        if bom[component]["suppliers"][supplier]["lead_time"] > assembly_start_week:
            model += x[(component, supplier)] == 0

# Solve the model
model.solve()

# Print results
print("Status:", pulp.LpStatus[model.status])
print("\nProcurement Plan:")
total_cost = 0
for component in bom:
    for supplier in bom[component]["suppliers"]:
        qty = x[(component, supplier)].value()
        if qty > 0:
            cost = bom[component]["suppliers"][supplier]["cost"]
            print(f"{component} from Supplier {supplier}: {qty} units")
            total_cost += qty * cost

print("\nTotal Cost:", total_cost)