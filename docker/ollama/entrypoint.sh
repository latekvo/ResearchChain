#!/bin/bash

/bin/ollama serve &

pid=$!

sleep 5

ollama pull zephyr:7b-beta-q5_K_M
ollama pull nomic-embed-text

wait $pid