#Shehan part starts

import tkinter as tk
from tkinter import messagebox
import random
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
import numpy as np

# Initialize Factor Graph
fg = FactorGraph()

# Defining the variables: Health, Reputation, Quest Progress, and Location
fg.add_nodes_from(['Health', 'Reputation', 'Quest Progress', 'Location', 'Combat Ability'])

# Defining the probabilistic relationships between these variables
health_factor = DiscreteFactor(['Health'], [3], [0.2, 0.5, 0.3])  # Probabilities for Low, Medium, High health
reputation_factor = DiscreteFactor(['Reputation'], [3], [0.5, 0.3, 0.2])  # Probabilities for Low, Neutral, High
quest_factor = DiscreteFactor(['Quest Progress'], [3], [0.6, 0.3, 0.1])  # Probabilities for quest stages
combat_factor = DiscreteFactor(['Combat Ability'], [3], [0.3, 0.5, 0.2])  # Low, Medium, High combat ability

# Add factors to the graph
fg.add_factors(health_factor, reputation_factor, quest_factor, combat_factor)

# Define dependencies between the variables
fg.add_edge('Health', 'Reputation')  # Health influences Reputation
fg.add_edge('Reputation', 'Quest Progress')  # Reputation influences Quest Progress
fg.add_edge('Health', 'Combat Ability')  # Health influences Combat Ability

# Initialize the game state
game_state = {
    "Health": 1,  # Default: Medium health
    "Reputation": 1,  # Default: Neutral reputation
    "Quest Progress": 0,  # Default: Not started
    "Location": "Not Selected",  # Starting location
    "Inventory": ["Map", "Potion"],  # Starting inventory
    "Combat Ability": 1,  # Default: Medium combat ability
}

# Tkinter setup
root = tk.Tk()
root.title("Adventure Quest")

# Game Labels
health_label = tk.Label(root, text="Health: " + str(game_state["Health"]))
health_label.pack()

reputation_label = tk.Label(root, text="Reputation: " + str(game_state["Reputation"]))
reputation_label.pack()

quest_label = tk.Label(root, text="Quest Progress: " + str(game_state["Quest Progress"]))
quest_label.pack()

location_label = tk.Label(root, text="Location: " + game_state["Location"])
location_label.pack()

inventory_label = tk.Label(root, text="Inventory: " + ", ".join(game_state["Inventory"]))
inventory_label.pack()

story_label = tk.Label(root, text="Welcome to the Adventure Quest!", wraplength=300)
story_label.pack()
#Shehan part ends
#Niloy push from here
