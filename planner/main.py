import os

# -------------------------
# 1. SIMULATED SENSOR INPUT
# -------------------------
temperature = 14  # change this to test

# -------------------------
# 2. SELECT PROBLEM FILE
# -------------------------
if temperature > 30:
    problem_file = "Problem1_Hot.pddl"
elif temperature < 18:
    problem_file = "Problem2_Cold.pddl"
else:
    problem_file = None

domain_file = "domain.pddl"

print(f"[INFO] Using domain: {domain_file}")
print(f"[INFO] Using problem: {problem_file}")

# -------------------------
# 3. "PLANNER" (SIMULATION)
# -------------------------
# Since Fast Downward is not installed yet,
# we simulate the plan based on problem file name

if problem_file == "Problem1_Hot.pddl":
    # ideally plan would be calculated by a planner like Fast downward. Here we are just 
    plan = [
        "turn-on-cooler",
        "cool-room"
    ]

elif problem_file == "Problem2_Cold.pddl":
    plan = [
        "turn-on-heater",
        "heat-room"
    ]

else:
    plan = []

# Save plan like a real planner would
with open("sas_plan", "w") as f:
    for action in plan:
        f.write(action + "\n")

print("[INFO] Plan generated")

# -------------------------
# 4. READ PLAN
# -------------------------
if os.path.exists("sas_plan"):
    with open("sas_plan", "r") as f:
        actions = [line.strip() for line in f.readlines()]
else:
    actions = []

# -------------------------
# 5. EXECUTE PLAN
# -------------------------
print("\n--- EXECUTING PLAN ---")

for action in actions:

    if action == "turn-on-cooler":
        print("Cooling system ON")

    elif action == "cool-room":
        print("Room cooled → NORMAL")

    elif action == "turn-on-heater":
        print("Heating system ON")

    elif action == "heat-room":
        print("Room heated → NORMAL")

print("\n[DONE]")