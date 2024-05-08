# Dino Bot using NEAT
 This project used [NEAT](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf "Original NEAT Research") (NeuroEvolution of Augmenting Topologies) an algorithm known for mimicing natural evolution based on the concept of the **Fittest** specimen in order to develop nerual networks to beat the [Google Dinosaur Game](https://chrome-dino-game.github.io/ "Example Game").

 Statistical Analysis was used to determine the most effective population size and Inputs needed to generate the most efficient neural network. 


## Project

### Demo

### Branch Specifications
Multiple branches were formed to store the state of the project at different stages.
1. **NEAT**: This is the default branch which runs the program seen in the Demo and used for the [Results](tab=readme-ov-file#res "Results Section")
2. **AI+ducking**: This branch has an AI which directly branched off the base game and determines it's course of action based on the highest of the 3 outputs (Jump, Duck, Run). The reason this is it's own seperate branch is because as noted in the [Results](tab=readme-ov-file#res "Results Section") section, the dinosaurs were never able to reliably develop a nerual network which allowed them to duck under the high birds and this resulted in stagnation in evolution for 10s of generations. Many different input combinations and population sizes were tried but it always resulted in stagnation of progress. 
3. **BaseGame**: This is the basic GUI implementation of the game which allows you to control the dinosaur as a player. 

---

### How to Replicate Project
1. Make sure your Local Machine has [Python](https://www.python.org/downloads/ "Python Download") installed and an IDE like [VS Code](https://code.visualstudio.com/download "VS Code Download").
2. Clone the repository onto your Local Machine
3. Use a Virtual Enviroment or use the IDE to run the project by running `main.py`
4. For Virtual Machine: First navigate to the derictory where the repo was cloned in the terminal and then use the following code to start the VM, install pygame and run the program:
```bash
    python -m venv venv
    venv\Scripts\activate 
    pip install pygame  
    python main.py
```

## Results

## Resources Used
* [NEAT-Python](https://neat-python.readthedocs.io/en/latest/index.html "Documentation") : NEAT Python Library used from the "AI" of this project
* [Pygame](https://www.pygame.org/news "Pygame Website") : Graphical Interface used to display the Dino game
* [Tutorial](https://www.youtube.com/watch?v=KOBKkPWGP-g&t=2s "YouTube") : Since this is my first use of pygame, this video guided me on how to build the basic framework of the game
  
## Steps to Build Upon
* Modify the NEAT algorithm and fitness function to allow the Dinosaurs to have an option to duck along with jump without causing stagnation. 