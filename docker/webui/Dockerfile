FROM condaforge/miniforge3

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    clang \
    && rm -rf /var/lib/apt/lists/*

RUN conda env create -f environment.yml

EXPOSE 8000

SHELL ["conda", "run", "-n", "ResearchChain", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ResearchChain", "python3", "main.py", "-w", "webui"]
