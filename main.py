import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import networkx as nx
import random
import matplotlib.colors as mcolors

num_of_iteration = 0
news_cred = {
    'number_of_likes': 0,
    'number_of_shares': 0
}
time_steps = [0]
percentages = [0]
simulation_running = False  # Flag to control continuous simulation

def create_random_graph(num_nodes, prob):
    global G
    G = nx.Graph()  # Create an empty graph
    for i in range(num_nodes):
        G.add_node(i, num_times_watch_news=0, num_times_liked_news=0, infection_rate=0.0,
                   fact_checking=random.uniform(0, 1),
                   political_agree=random.uniform(0, 1))  # Add nodes with attributes

    for u in range(num_nodes):
        for v in range(u + 1, num_nodes):
            if random.uniform(0, 1) < prob:
                weight = random.uniform(0, 1)
                G.add_edge(u, v, weight=weight)  # Add edges with weights
    return G


def share_news():
    shares_scale = float(share_rate_slider.get())
    likes_scale = float(like_rate_slider.get())
    for node in G.nodes:
        if G.nodes[node]["infection_rate"] > 8:
            neighbors = list(G.neighbors(node))
            num_neighbors_to_share = random.randint(1, len(neighbors))  # Choose a random number of neighbors
            selected_neighbors = random.sample(neighbors, num_neighbors_to_share)  # Randomly select neighbors

            news_cred['number_of_shares'] += 1
            for neighbor in selected_neighbors:
                weight = G[node][neighbor]["weight"]
                G.nodes[neighbor]["num_times_watch_news"] += 1
                change_rate = G.nodes[neighbor]["num_times_watch_news"] * weight \
                              * (1 - G.nodes[neighbor]["fact_checking"]) \
                              * ((1 + min(1, shares_scale * news_cred['number_of_shares'] / num_nodes))) \
                              * ((1 + likes_scale * news_cred['number_of_likes'] / num_nodes)) \
                              * G.nodes[neighbor]["political_agree"]
                print(neighbor, G.nodes[neighbor], news_cred, num_nodes, weight)
                G.nodes[neighbor]["infection_rate"] += change_rate
                G.nodes[neighbor]["infection_rate"] = G.nodes[neighbor]["infection_rate"] = max(
                    min(round(G.nodes[neighbor]["infection_rate"], 2), 10), 0)

                if G.nodes[neighbor]["infection_rate"] > 5 and G.nodes[neighbor]["num_times_liked_news"] == 0 and \
                        G.nodes[neighbor]["political_agree"] > 0.5:
                    # Increment the number of likes in news_cred
                    news_cred['number_of_likes'] += 1
                    # Mark the node as having liked the news
                    G.nodes[neighbor]["num_times_liked_news"] = 1
    fully_infected_count = sum(1 for node in G.nodes if G.nodes[node]["infection_rate"] == 10)
    percentage_fully_infected = (fully_infected_count / num_nodes) * 100
    time_steps.append(time_steps[-1] + 1)
    percentages.append(percentage_fully_infected)
    update_line_chart()

# Initialize the graph
num_nodes = 20
prob = 0.3

G = create_random_graph(num_nodes, prob)
node_colors = [0] * num_nodes

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # 1 row, 2 columns
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, ax=ax1,node_color=node_colors, cmap=plt.cm.Reds, node_size=300)

# Create a Tkinter window
root = tk.Tk()
root.title("Fake News Spread Simulation")

# Create a canvas for Matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a line chart on ax2
ax2.grid()
ax2.plot(time_steps, percentages, marker='o', linestyle='-')
ax2.set_xlabel('Time Steps')
ax2.set_ylabel('Percentage of Fully Infected Nodes')
ax2.set_xlim(0, 10)  # Adjust the initial limits as needed
ax2.set_ylim(0, 100)
ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))




def init_graph():
    global num_nodes, prob,time_steps,percentages
    num_nodes = int(nodes_slider.get())
    prob = float(prob_slider.get())
    G = create_random_graph(num_nodes, prob)
    patient_zero = 0
    G.nodes[patient_zero]['infection_rate'] = 10
    time_steps = [0]
    percentages = [0]
    update_graph()


def infection_rate_color(rate):
    if rate == 10:
        return mcolors.to_rgba("red", alpha=1)  # Dark red when infection rate is 10
    else:
        # Use a custom colormap for other values, mapping from 0 to 10
        colormap = plt.get_cmap('Oranges')
        normalized_rate = rate / 10.0  # Normalize rate to 0-1
        return colormap(normalized_rate)


def update_graph():
    ax1.clear()
    # Get the infection rates of all nodes
    infection_rates = [G.nodes[node]["infection_rate"] for node in G.nodes]
    # Map infection rates to colors using the custom function
    node_colors = [infection_rate_color(rate) for rate in infection_rates]
    pos = nx.spring_layout(G, seed=42)

    # Access edge weights and set edge colors based on a colormap
    edge_weights = [G.get_edge_data(u, v)['weight'] for u, v in G.edges]
    edge_cmap = plt.get_cmap('Blues')  # Choose a colormap for edges, e.g., 'Blues'
    edge_colors = [edge_cmap(weight) for weight in edge_weights]
    nx.draw(G, pos,ax=ax1, node_color=node_colors, node_size=300, edge_color=edge_colors)
    labels = {node: G.nodes[node]["infection_rate"] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, ax=ax1,font_size=9, font_color='black')
    calculate_network_metrics()

    canvas.draw()


def reset():
    global G, num_of_iteration, time_steps,percentages
    num_of_iteration = 0
    patient_zero = 0
    for node in G.nodes:
        G.nodes[node]['num_times_watch_news'] = 0
        G.nodes[node]['num_times_liked_news'] = 0
        if node == patient_zero:
            G.nodes[node]['infection_rate'] = 10.0
        else:
            G.nodes[node]['infection_rate'] = 0.0
    global news_cred
    news_cred = {
        'number_of_likes': 0,
        'number_of_shares': 0
    }
    time_steps = [0]
    percentages = [0]
    update_graph()


def go_once():
    global num_of_iteration
    num_of_iteration = num_of_iteration + 1
    print('Iteration: ' + str(num_of_iteration))
    share_news()
    update_graph()


def update_line_chart():
    global time_steps, percentages
    ax2.clear()
    ax2.plot(time_steps, percentages, marker='o', linestyle='-')
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Percentage of Fully Infected Nodes')
    ax2.set_xlim(0, len(time_steps) - 1)
    ax2.set_ylim(0, 100)
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax2.grid()
    for i, (x, y) in enumerate(zip(time_steps, percentages)):
        ax2.text(x, y, f'{y:.2f}%', fontsize=9, va='bottom', ha='center', color='blue')

def start_simulation():
    global simulation_running
    simulation_running = True
    simulate_continuous()

def stop_simulation():
    global simulation_running
    simulation_running = False

def simulate_continuous():
    if simulation_running:
        go_once()
        root.after(100, simulate_continuous)  # Repeat the simulation after a delay (1 second)

# Calculate and display degree distribution, clustering coefficient, and average path length
def calculate_network_metrics():
    degree_dist = nx.degree_histogram(G)
    clustering_coefficient = nx.average_clustering(G)
    average_path_length = nx.average_shortest_path_length(G)
    
    # Display the calculated metrics above the network diagram
    metrics_text = f"Degree Distribution: {degree_dist}\n"
    metrics_text += f"Clustering Coefficient: {clustering_coefficient:.4f}\n"
    metrics_text += f"Average Path Length: {average_path_length:.4f}\n"
    metrics_label.config(text=metrics_text)


# Label to display network metrics
metrics_label = Label(root, text="Network Characteristics", justify=LEFT)
metrics_label.pack(side=RIGHT, padx=20, pady=10)

# Create sliders to modify parameters
slider_frame = Frame(root)
slider_frame.pack(side=LEFT, padx=10, pady=10)

nodes_label = Label(slider_frame, text="Number of Nodes")
nodes_slider_var = StringVar()
nodes_slider = Scale(slider_frame, from_=1, to=200, variable=nodes_slider_var, orient="horizontal", length=200)
nodes_slider.set(num_nodes)
nodes_label.pack()
nodes_slider.pack()

prob_label = Label(slider_frame, text="Link Probability")
prob_slider_var = StringVar()
prob_slider = Scale(slider_frame, from_=0.1, to=1.0, variable=prob_slider_var, digits=3, resolution=0.01, orient="horizontal", length=200)
prob_slider.set(prob)
prob_label.pack()
prob_slider.pack()

social_frame = Frame(root)
social_frame.pack(side=LEFT, padx=10, pady=10)

like_rate_label = Label(social_frame, text="Like scale")
like_slider_var = StringVar()
like_rate_slider = Scale(social_frame, from_=0.0, to=1.0, variable=like_slider_var, digits=3, resolution=0.01, orient="horizontal", length=200)
like_rate_slider.set(0.2)
like_rate_label.pack()
like_rate_slider.pack()

share_rate_label = Label(social_frame, text="Share scale")
share_slider_var = StringVar()
share_rate_slider = Scale(social_frame, from_=0.0, to=1.0, variable=share_slider_var, digits=3, resolution=0.01, orient="horizontal", length=200)
share_rate_slider.set(0.1)
share_rate_label.pack()
share_rate_slider.pack()

# Create buttons
button_frame = Frame(root)
button_frame.pack(side=LEFT, padx=10, pady=20)

update_button = tk.Button(button_frame, text="Update Graph", command=init_graph)
update_button.pack()

go_once_button = tk.Button(button_frame, text="Go Once", command=go_once)
go_once_button.pack()

reset_button = tk.Button(button_frame, text="Reset", command=reset)
reset_button.pack()

# Add "Start Simulation" and "Stop Simulation" buttons
start_button = tk.Button(button_frame, text="Start Simulation", command=start_simulation)
start_button.pack()

stop_button = tk.Button(button_frame, text="Stop Simulation", command=stop_simulation)
stop_button.pack()

# Initialize a variable to track the simulation state
simulation_running = False


# Run the Tkinter main loop
root.mainloop()
