# Fake News Spread Simulation
This Python program simulates the spread of fake news in a network of nodes. The network is represented as a graph, with nodes and edges, using the NetworkX library. The simulation is displayed in a graphical user interface (GUI) using Tkinter and Matplotlib.

## Prerequisites
Before running the simulation, make sure you have the following libraries installed:

* Tkinter
* Matplotlib
* NetworkX

You can install these libraries using pip if you haven't already.
```
pip install tkinter
pip install matplotlib
pip install networkx
```
## Running the Simulation
To run the simulation, execute the main.py script.
```
python main.py
```
This will open the GUI window for the simulation.

## Simulation Parameters
### Network Setup
* Number of Nodes: Adjust the number of nodes in the network using the "Number of Nodes" slider. This controls the size of the simulated network.

* Link Probability: Set the link probability to determine the likelihood of a connection between nodes. Higher values create denser networks, while lower values result in sparser networks.

### Simulation Controls
* Update Network: Click the "Update Network" button to create a new random network. This action resets the simulation.

* Go Once: Click the "Go Once" button to perform a single step of the simulation. In this step, nodes with a high infection rate can share news with their neighbors, and the infection rate of other nodes is updated based on several factors, such as fake news quality, likes, and shares.

* Reset: Click the "Reset" button to reset the simulation to its initial state, but keep the same network structure.

* Start simulation: Click the "Start simulation" button to keep the simulation running, instead of go once every iteration.

* Stop simulation: click the "Stop simulation" button to stop simulation
### Infection Rate Colors
* Nodes are colored based on their infection rates.
* Nodes with an infection rate of 1.0 are displayed in dark red.
* Nodes with lower infection rates are color-coded using the "Reds" colormap, with shades of red.
### Like and Share Rates
* The simulation introduces two new sliders, "Infection-to-Like Rate" and "Infection-to-Share Rate."
* These sliders control how quickly infection rates grow when nodes like or share news.
* Smaller values for these rates will slow down infection rate growth.
### Simulation Logic
* Nodes in the network have various attributes, including infection rates, fact-checking abilities, and political agreement.
* The simulation starts with a random network structure.
* One node is designated as "patient zero" with a high infection rate, while others start with lower infection rates.
* Nodes can share news based on their infection rates, and the spread is influenced by factors such as fake news quality, likes, shares, and fact-checking abilities.
### Acknowledgments
This simulation is for educational purposes and can be modified to explore various scenarios and parameters related to information spread in networks.

Feel free to experiment with the simulation, and modify the code to suit your needs or conduct research on information diffusion in networks.