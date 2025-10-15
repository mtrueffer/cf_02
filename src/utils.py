import csv

def load_unit_stats(filepath):
    unit_stats = {}
    with open(filepath,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            faction = row["faction"]
            name = row["name"]
            if faction not in unit_stats:
                unit_stats[faction] = {}
            unit_stats[faction][name] = {
                "type": row["type"],
                "speed": float(row["speed"]),
                "health": int(row["health"]),
                "damage": int(row["damage"]),
                "damage_type": row["damage_type"],
                "attack_rate": float(row["attack_rate"]),
                "range": int(row["range"]),
                "armor": int(row["armor"]),
                "armor_type": row["armor_type"],
                "spawn_rate": float(row["spawn_rate"])
            }
    return unit_stats

def load_building_stats(filepath):
    building_stats = {}
    with open(filepath,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row = reader:
            faction = row["faction"]
            name = row["name"]
            if faction not in building_stats:
                building_stats[faction] = {}
            building_stats[faction][name] = {
                "type": row["type"],
                "cost": int(row["cost"]),
                "health": int(row["health"]),
                "damage": int(row["damage"]),
                "damage_type": row["damage_type"],
                "attack_rate": float(row["attack_type"]),
                "range": int(row["range"]),
                "spawn_rate": float(row["spawn_rate"])
            }
    return building_stats

def have_same_sign(a, b):
    return (a >= 0 and b>= 0) or (a < 0 and b < 0)

def distance(A, B):
    return ((B[0]-A[0])**2 + (B[1]-A[1])**2)**0.5

def norm_dist(A, B):
    dist = distance(A, B)
    if dist == 0:
        return 0, 0
    return (B[0]-A[0])/dist, (B[1]-A[1])/dist

def dot_prod(A, B):
    return A[0]*B[0] + A[1]*B[1]
