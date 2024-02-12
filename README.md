# ResearchChain
#### Langchain project aiming at achieving perpetual research with the help of a chain of ai researching agents.

* Install and launch Ollama: `ollama serve`
* Create new environment: `conda env create -f environment.yml`
* Activate the new environment: `conda activate ResearchChain`
* Pull the model you intend to use: `ollama pull zephyr:7b-beta-q5_K_M` (default)
* Run: `python3 main.py`

The default model is hardcoded into the `lookup.py` file.