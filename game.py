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
#Niloy Part Starts

# Update game state labels
def update_labels():
    health_label.config(text="Health: " + str(game_state["Health"]))
    reputation_label.config(text="Reputation: " + str(game_state["Reputation"]))
    quest_label.config(text="Quest Progress: " + str(game_state["Quest Progress"]))
    location_label.config(text="Location: " + game_state["Location"])
    inventory_label.config(text="Inventory: " + ", ".join(game_state["Inventory"]))

# Function to allow the player to choose their starting location
def choose_starting_location(location_choice):
    game_state["Location"] = location_choice
    update_labels()
    story_label.config(text=f"You have chosen to start at {location_choice}. Your journey begins!")

    # Hide location choice buttons after selection
    location_buttons_frame.pack_forget()
    show_location_choices(game_state["Location"])
    
# Function to show available choices based on the location
def show_location_choices(location):
    location_choices = []
    if location == "Lalbagh Fort":
        location_choices = ["Explore the Hidden Passage", "Leave the Fort", "Rest and Heal", "Random Event"]
    elif location == "Sadarghat":
        location_choices = ["Approach the Merchant", "Leave the Area", "Random Event"]
    elif location == "National Museum":
        location_choices = ["Investigate the Museum", "Leave the Museum"]
    elif location == "Sundarbans":
        location_choices = ["Explore the Forest", "Leave the Forest", "Fight Wild Animals", "Random Event"]
    elif location == "Ahsan Manzil":
        location_choices = ["Explore the Mansion", "Leave the Mansion", "Meet the Local NPC"]

for choice in location_choices:
        action_button = tk.Button(root, text=choice, command=lambda c=choice: update_game_state(c))
        action_button.pack()

#Niloy Part Ends
