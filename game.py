#Shehan Starts-------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import random
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
import numpy as np

# Initialize Factor Graph
fg = FactorGraph()

# Defining the variables: Health, Reputation, Combat Ability, Quest Progress
fg.add_nodes_from(['Health', 'Reputation', 'Combat Ability', 'Quest Progress', 'FightOutcome', 'NegotiationOutcome'])

# Define the probabilities for each variable
health_factor = DiscreteFactor(['Health'], [3], [0.2, 0.5, 0.3])  # Low, Medium, High health
reputation_factor = DiscreteFactor(['Reputation'], [3], [0.5, 0.3, 0.2])  # Low, Neutral, High reputation
combat_factor = DiscreteFactor(['Combat Ability'], [3], [0.3, 0.5, 0.2])  # Low, Medium, High combat ability
quest_factor = DiscreteFactor(['Quest Progress'], [3], [0.6, 0.3, 0.1])  # Quest stages

# Fight and Negotiation outcomes based on Combat Ability and Reputation
fight_prob_table = [
    [0.8, 0.2],  # CombatAbility = 0 (low)
    [0.5, 0.5],  # CombatAbility = 1 (medium)
    [0.1, 0.9]   # CombatAbility = 2 (high)
]

nego_prob_table = [
    [0.7, 0.3],  # Reputation = 0 (low)
    [0.4, 0.6],  # Reputation = 1 (medium)
    [0.1, 0.9]   # Reputation = 2 (high)
]

# Create factors for fight and negotiation outcomes
fight_factor = DiscreteFactor(['Combat Ability', 'FightOutcome'], [3, 2], sum(fight_prob_table, []))
nego_factor = DiscreteFactor(['Reputation', 'NegotiationOutcome'], [3, 2], sum(nego_prob_table, []))

fg.add_factors(health_factor, reputation_factor, combat_factor, quest_factor, fight_factor, nego_factor)

# Define dependencies between the variables
fg.add_edges_from([
    ('Health', health_factor),
    ('Reputation', reputation_factor),
    ('Combat Ability', combat_factor),
    ('Quest Progress', quest_factor),
    ('Combat Ability', fight_factor),
    ('FightOutcome', fight_factor),
    ('Reputation', nego_factor),
    ('NegotiationOutcome', nego_factor),
])

# Game state initialization
game_state = {
    "Health": 5,  # Default: Medium health
    "Reputation": 1,  # Default: Neutral reputation
    "Quest Progress": 0,  # Default: Not started
    "Location": None,  # Starting location is None
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

location_label = tk.Label(root, text="Location: " + (game_state["Location"] if game_state["Location"] else "Not Selected"))
location_label.pack()

inventory_label = tk.Label(root, text="Inventory: " + ", ".join(game_state["Inventory"]))
inventory_label.pack()

story_label = tk.Label(root, text="Welcome to the Adventure Quest!", wraplength=300)
story_label.pack()

# Initialize action_buttons_frame to hold the action buttons (initially empty)
action_buttons_frame = tk.Frame(root)

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

#Shehan Part ends-----------------------------------------------------------------------------
#Push from here guys
#Niloy Starts---------------------------------------------------------------------------------

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





    # Clear previous buttons before creating new ones
    for widget in action_buttons_frame.winfo_children():
        widget.destroy()

    # Create new action buttons
    for choice in location_choices:
        action_button = tk.Button(action_buttons_frame, text=choice, command=lambda c=choice: update_game_state(c))
        action_button.pack()

    # Pack the action_buttons_frame to show it
    action_buttons_frame.pack()

# Function to update the game state
def update_game_state(action):
    if game_state["Health"] <= 0:
        game_over()

    if action == "Explore the Hidden Passage":
        game_state["Health"] -= 1
        update_labels()
        story_label.config(text="You explore the Hidden Passage but lose some health.")
    
    elif action == "Rest and Heal":
        game_state["Health"] = min(game_state["Health"] + 3, 10)
        update_labels()
        story_label.config(text="You rest and heal. Your health is restored.")

    elif action in ["Leave the Fort", "Leave the Area", "Leave the Museum", "Leave the Forest", "Leave the Mansion"]:
        story_label.config(text=f"You leave the {game_state['Location']}.")
        choose_new_location()

    elif action == "Random Event":
        random_event()

    elif action == "Fight Wild Animals" or action == "Fight Bandits":
        combat_outcome()

    elif action == "Approach the Merchant":
        approach_merchant()

# Function to simulate the Merchant encounter
def approach_merchant():
    story_label.config(text="You approach the merchant. He offers a rare item for 5 gold coins.")
    action_buttons_frame.pack_forget()
    merchant_frame = tk.Frame(root)
    merchant_frame.pack()

    buy_button = tk.Button(merchant_frame, text="Buy Item", command=lambda: buy_item(merchant_frame))
    buy_button.pack()

    leave_button = tk.Button(merchant_frame, text="Leave", command=lambda: leave_merchant(merchant_frame))
    leave_button.pack()

#Niloy Part Ends-----------------------------------------------------------
