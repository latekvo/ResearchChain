# ResearchChain

#### Langchain project aiming at achieving perpetual research with the help of a chain of ai researching agents.

- Install and launch Ollama: `ollama serve`
- Create new environment: `conda env create -f environment.yml`
- Activate the new environment: `conda activate ResearchChain`
- Pull the model you intend to use: `ollama pull zephyr:7b-beta-q5_K_M` (default)
- Pull an embedding model you: `ollama pull nomic-embed-text` (default)
- Run: `python3 main.py`

#### Other notes

- The default models are hardcoded in the `core/models` folder.<br>
- We're using python version `3.9`

## This project consists of 3 separate elements

> #### Research Chain
> Receives and completes basic summary task.<br>
It's built as a loop, with integrated perpetual crawler, web analyzer and embedder,<br>
to populate its RAG database with any lacking data that it may require.<br>
It's a standalone service composed of 5 databases and 4 containers,
each independently scalable.<br>

> #### Web Interface
> Human-readable way to interact with every element of Research Chain

> #### Research Loop
> AI powered service automatically dispatching, analyzing and managing Research Chain.<br>
It should work along side Web Interface, to supply constant 24/7 news analysis,
and to expand it's knowledge base by scheduling crawls based on the provided areas of interest

---
### Contributing

If you'd like to contribute to this project, 
feel free to reach out to us through my telegram: `https://t.me [slash] latkaignacy`.<br>
In such case, we'll introduce you into this project, and help you find a good first issue.

---

THIS SOFTWARE IS INTENDED FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.
WE ARE NOT RESPONSIBLE FOR ANY ILLICIT USES OF THIS SOFTWARE.
