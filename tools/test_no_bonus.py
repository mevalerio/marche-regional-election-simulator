import pandas as pd
from math import floor

def dhondt(values, seats):
    if seats <= 0 or sum(values.values()) <= 0:
        return {k:0 for k in values}
    qs=[]
    for k,v in values.items():
        for d in range(1,seats+1):
            qs.append((k, v/d))
    qs.sort(key=lambda x:x[1], reverse=True)
    win=[k for k,_ in qs[:seats]]
    return {k:win.count(k) for k in values}

# Test D'Hondt without minimum bonus
centrodestra_votes = 295800
centrosinistra_votes = 285427
total_seats = 30

print("=== D'HONDT WITHOUT BONUS ===")
result = dhondt({"Centrodestra": centrodestra_votes, "Centrosinistra": centrosinistra_votes}, total_seats)
print(f"Centrodestra: {result['Centrodestra']} seats")
print(f"Centrosinistra: {result['Centrosinistra']} seats")

print("\n=== WITH MINIMUM BONUS (48.93% -> 19 seats) ===")
print("Centrodestra: 19 seats (minimum bonus)")
print("Centrosinistra: 11 seats (remaining)")

print(f"\n=== PROPORTIONAL CHECK ===")
ratio = centrosinistra_votes / centrodestra_votes
print(f"Vote ratio (CS/CD): {ratio:.3f}")
print(f"Seat ratio without bonus (CS/CD): {result['Centrosinistra']}/{result['Centrodestra']} = {result['Centrosinistra']/result['Centrodestra']:.3f}")
print(f"Seat ratio with bonus (CS/CD): 11/19 = {11/19:.3f}")
