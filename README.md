# ResearchChain
#### Langchain project aiming at achieving perpetual research with the help of a chain of ai researching agents.

* Install and launch Ollama: `ollama serve`
* Create new environment: `conda env create -f environment.yml`
* Activate the new environment: `conda activate ResearchChain`
* Pull the model you intend to use: `ollama pull zephyr:7b-beta-q5_K_M` (default)
* Run: `python3 main.py`
#### Other notes
The default model is hardcoded into the `lookup.py` file.

# Future of this project
## I want to convert this project into 3 layers of separate complexity.
#### Research Chain
A set of tools to give LLMs research capabilities.
#### Research Tree
A recursive tree structure granting Research Chain the ability 
to create large hierarchical structures of LLMs and the tools they are using 
#### Research Loop
A service launching for a set period of time, and then allowing the user to summarize
either the entire output of the tree, or a small, selected subset of it's structure.
