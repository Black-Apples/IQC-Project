Sure, here is the README content in text format:

---

## README

# Introduction to Quantum Computing - Project Report

## Project Overview

This project report covers the topic of quantum algorithms for the Elemental Distinctness problem, focusing on Grover's Search and Quantum Walks. The report is prepared by Aakarsh Jain, Raghav Sakhuja, and Siddhant Rai Viksit from IIIT - Delhi.

## Contents

1. Introduction
2. Grover Search for Elemental Distinctness
   - Algorithm
   - Oracle for Grover Search
   - Analysis
   - Result
3. Quantum Walk for Elemental Distinctness
   - Quantum Walk
   - Algorithm
   - Implementation
   - Results

## Authors

- Aakarsh Jain (Roll Number - 2021507) [aakarsh21507@iiitd.ac.in](mailto:aakarsh21507@iiitd.ac.in)
- Raghav Sakhuja (Roll Number - 2021274) [raghav21274@iiitd.ac.in](mailto:raghav21274@iiitd.ac.in)
- Siddhant Rai Viksit (Roll Number - 2021565) [siddhant21565@iiitd.ac.in](mailto:siddhant21565@iiitd.ac.in)

## Report Highlights

### 1. Introduction

Elemental Distinctness Problem: Given numbers \(x_1, ..., x_N \in [N]\), determine if all numbers are distinct. The report explores quantum algorithms to solve this problem more efficiently than classical algorithms.

### 2. Grover Search for Elemental Distinctness

- **Algorithm**: Utilizes Grover's search algorithm to solve the problem in \(O(N^{3/4})\) queries, significantly improving over the classical \(O(N)\) queries.
- **Oracle for Grover Search**: Defines unitary operations \(U_{copy}\) and \(U_{comp}\) to construct the oracle required for Grover's algorithm.
- **Analysis**: The algorithm's time complexity and success probability are analyzed, demonstrating its efficiency.
- **Result**: Python implementation and results of tests on an array of size \(N = 100\).

### 3. Quantum Walk for Elemental Distinctness

- **Quantum Walk**: Describes the use of quantum superposition states to explore multiple paths simultaneously in a graph.
- **Algorithm**: Constructs a Johnson graph and defines a quantum walk algorithm for the Elemental Distinctness problem.
- **Implementation**: Implementation using Qiskit and a 4D hypercube example.
- **Results**: Results of the simulation are presented, showing consistency with theoretical expectations.

## Running the Experiments

### Grover Search Experiment

1. Clone the repository: `git clone https://github.com/Black-Apples/IQC-Project`
2. Navigate to the project directory: `cd IQC-Project`
3. Set up a virtual environment:
   ```bash
   python3 -m venv ./.venv
   source ./.venv/bin/activate
   ```
4. Install the required packages: `pip install -r requirements.txt`
5. Run the Grover search script: `python3 elemental_distinctiveness.py`

### Quantum Walk Experiment

1. Clone the repository: `git clone https://github.com/Black-Apples/IQC-Project`
2. Navigate to the project directory: `cd IQC-Project`
3. Set up a virtual environment:
   ```bash
   python3 -m venv ./.venv
   source ./.venv/bin/activate
   ```
4. Install the required packages: `pip install -r requirements.txt`
5. Run the quantum walk script: `python3 quantumwalk_hypercube.py`

## References

1. Andris Ambainis. "Quantum search algorithms." 2005. [arXiv:quant-ph/0504012](https://arxiv.org/abs/quant-ph/0504012)
2. Andris Ambainis. "Quantum walk algorithm for element distinctness." SIAM Journal on Computing 37.1 (2007): 210–239.

For more details, refer to the full project report available in the repository.

## Repository Links

- [Project Repository](https://github.com/Black-Apples/IQC-Project)
- [Qiskit Textbook](https://github.com/Qiskit/textbook/tree/main) for Quantum Walk implementation

Feel free to reach out to any of the authors for questions or further discussion about the project.

---
