import random

# -----------------------------
# Factor Graph Implementation
# -----------------------------

class VariableNode:
    def __init__(self, name, states):
        self.name = name
        self.states = states
        # Start with a uniform belief distribution
        self.belief = {state: 1.0 / len(states) for state in states}
    
    def __str__(self):
        return f"{self.name}: {self.belief}"

class FactorNode:
    def __init__(self, name, variables, potential_func):
        self.name = name
        self.variables = variables  # List of connected variable nodes
        self.potential_func = potential_func  # A function representing the potential

    def compute_message(self, target_variable):
        
        message = {}
        for state in target_variable.states:
            # For simplicity, assume the potential function modifies the belief directly.
            # In a more sophisticated implementation, you would sum/integrate over
            # all other variables' states.
            product = self.potential_func({target_variable.name: state})
            # Multiply by current belief (for demonstration purposes)
            product *= target_variable.belief[state]
            message[state] = product
        # Normalize the message
        total = sum(message.values())
        for key in message:
            message[key] /= total if total > 0 else 1
        return message

class FactorGraph:
    def __init__(self):
        self.variable_nodes = {}
        self.factor_nodes = []
    
    def add_variable(self, name, states):
        node = VariableNode(name, states)
        self.variable_nodes[name] = node
        return node
    
    def add_factor(self, name, variables, potential_func):
        factor = FactorNode(name, variables, potential_func)
        self.factor_nodes.append(factor)
        return factor
    
    def belief_propagation(self):
        
        for factor in self.factor_nodes:
            for var in factor.variables:
                message = factor.compute_message(var)
                # Update variable belief: multiply current belief by the message and normalize
                for state in var.states:
                    var.belief[state] *= message[state]
                # Normalize belief for stability
                total = sum(var.belief.values())
                for state in var.states:
                    var.belief[state] /= total if total > 0 else 1

# -----------------------------
# Game Logic Implementation
# -----------------------------

def game_loop():
    print("Welcome to Adventure Quest: The Lost Artifact!")
    print("In the ancient kingdom of Eldoria, a prophecy foretells that the fate of the realm depends on retrieving the Heart of Eldoria.")
    print("You stand at a crossroads. Choose your path:")
    print("1. Venture into the Dark Forest")
    print("2. Traverse the Misty Mountains")
    
    choice = input("Enter 1 or 2: ").strip()
    
    # Create the factor graph
    fg = FactorGraph()
    
    # Create a variable node for the path decision
    path_node = fg.add_variable("Path", ["Forest", "Mountains"])
    
    # Set the prior belief based on player's input
    if choice == "1":
        path_node.belief = {"Forest": 0.9, "Mountains": 0.1}
    elif choice == "2":
        path_node.belief = {"Forest": 0.1, "Mountains": 0.9}
    else:
        print("Invalid choice, defaulting to Forest.")
        path_node.belief = {"Forest": 0.8, "Mountains": 0.2}
    
    # Create a variable node for an encounter outcome: whether you meet a talking wolf
    encounter_node = fg.add_variable("Encounter", ["Yes", "No"])
    
    # Define a potential function that links the chosen path to the chance of an encounter
    def encounter_potential(state_dict):
        # state_dict will have one key: either 'Path' or 'Encounter'
        if "Path" in state_dict:
            # When computing a message for the path, favor the forest if it leads to an encounter.
            if state_dict["Path"] == "Forest":
                return 1.2  # Higher potential if Forest is chosen
            else:
                return 0.8  # Lower potential if Mountains are chosen
        elif "Encounter" in state_dict:
            # When computing a message for the encounter outcome,
            # assume that a forest path increases the chance of meeting the wolf.
            if state_dict["Encounter"] == "Yes":
                return 1.3
            else:
                return 0.7
        return 1.0

    # Add a factor node connecting Path and Encounter decisions
    fg.add_factor("EncounterFactor", [path_node, encounter_node], encounter_potential)
    
    # Run belief propagation to update beliefs based on the factor graph
    fg.belief_propagation()
    
    # Display the updated beliefs
    print("\nUpdated Beliefs after your decision:")
    print(f"Path: {path_node.belief}")
    print(f"Encounter: {encounter_node.belief}")
    
    # Decide the encounter outcome based on the computed belief
    encounter_outcome = random.choices(
        encounter_node.states,
        weights=[encounter_node.belief[s] for s in encounter_node.states]
    )[0]
    
    if encounter_outcome == "Yes":
        print("\nAs you proceed, a mystical talking wolf emerges from the shadows!")
        print("The wolf offers you cryptic advice that might help you on your quest.")
        # Insert additional narrative logic or decision points here
    else:
        print("\nYour path remains silent. You continue your journey without any unusual encounters.")
        # Insert alternative narrative logic here
    
    print("\nThe adventure continues....more question will be added once we choose the appropriate story")

if _name_ == '_main_':
    game_loop()
