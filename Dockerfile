FROM condaforge/miniforge3

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    clang \
    && rm -rf /var/lib/apt/lists/*

RUN conda env create -n ResearchChain -f environment.yml

SHELL ["conda", "run", "-n", "ResearchChain", "/bin/bash", "-c"]

CMD ["conda", "run", "-n", "ResearchChain", "python3", "main.py", "-w", "crawler"]
