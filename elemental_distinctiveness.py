from qiskit import QuantumCircuit, Aer, transpile, assemble
import numpy as np
import warnings
# suppress the warnings
warnings.filterwarnings("ignore")


def grover_iterator(oracle,N)->QuantumCircuit:
    """Implement the Grover's iterator to solve the problem"""
    qc=QuantumCircuit(N)
    qc.append(oracle,range(N))
    # qc.barrier()
    qc.h(range(N))
    qc.x(range(N))
    qc.h(N-1)
    qc.mcx(list(range(N-1)),N-1)
    qc.h(N-1)
    qc.barrier()
    qc.x(range(N))
    qc.h(range(N))
    qc.barrier()
    return qc

def A(n)->QuantumCircuit:
    """Implement the A operator for generating the superposition of all states"""
    qc = QuantumCircuit(n)
    for qubit in range(n):
        qc.h(qubit)
    qc.barrier()
    return qc

def oracle(n, solution_indices):
    oracle = QuantumCircuit(n)

    oracle.barrier()
    for idx in solution_indices:
        # Convert idx to binary representation
        binary_rep = bin(idx)[2:].zfill(n-1)
        
        # print(binary_rep)
        # reverse the binary representation
        binary_rep = binary_rep[::-1]
        # Apply X gates on qubits where binary_rep is '1'
        for i, bit in enumerate(binary_rep):
            if bit == '0':
                oracle.x(i)

        # Apply multi-controlled X gate
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)
        # Unapply X gates
        for i, bit in enumerate(binary_rep):
            if bit == '0':
                oracle.x(i)
        
        oracle.barrier()

    # oracle.barrier()
    # print("Oracle circuit:")
    # print(oracle)
    return oracle

def grover_algorithm(n, k, A_circuit, grover_circuit):
    """Implement the Grover's algorithm for element distinctness problem"""
    # Creating the main circuit
    circuit=QuantumCircuit(n+1, n)
    # Adding the A operator to create the superposition of all states before passing to Grover's iterator
    circuit.append(A_circuit, range(n+1))
    # Adding the Grover's iterator
    for _ in range(k):
        circuit.append(grover_circuit, range(n+1))

    # measurement
    circuit.measure(range(n), range(n))

    # circuit.draw()

    # Running the circuit
    qasm_simulator = Aer.get_backend("qasm_simulator")
    transpiled_circuit = transpile(circuit, qasm_simulator)
    qobj = assemble(transpiled_circuit, shots=1)
    result = qasm_simulator.run(qobj).result()
    counts = result.get_counts()
    # print(counts)

    # Return the most probable state
    return max(counts, key=counts.get)

# Change this to define the array
N:int = 100
array=np.random.randint(N*2, size=N)
N:int = len(array)
np.random.shuffle(array)
# array = np.array([5, 7, 2, 2, 1, 3, 9, 9, 0, 7])
print(f"Initial Array: {array}")

# Pick random sqrt(N) elements
RootN:int = int(np.sqrt(N))
marked = array[:RootN]
print(f"Marked elements: {marked}")
if(len(set(marked))!=len(marked)):
    print("Marked elements are not unique, found duplicates")
    exit()

# Adding a dummy element to index 0
remaining = array[RootN:]
# remaining.extend()
print(f"Remaining elements: {remaining}")
T:int = len(remaining)
logT:int = int(np.ceil(np.log2(T)))

# Creating the oracle using the dupicates
solution_idx:list[int] = []
for i in marked:
    for j in range(len(remaining)):
        if i==remaining[j]:
            solution_idx.append(j)
print(f"Solution Index: {solution_idx}")
oracle_circuit:QuantumCircuit = oracle(logT+1, solution_idx)

grover:QuantumCircuit = grover_iterator(oracle_circuit,logT+1)
A_circuit:QuantumCircuit = A(logT+1)

# Running the Grover's algorithm for unknown theta
lambda_:int = 1.2
m:int = 2
no_of_calls=0
for _ in range(int(np.ceil(np.sqrt(N)))):
    k:int = np.random.randint(1, m)
    no_of_calls+=k
    result = grover_algorithm(logT, k, A_circuit, grover)
    print(f"Duplicate Index returned: {result}")
    result_idx = int(result, 2)
    try:
        print(f"Duplicate element: {remaining[result_idx]}")
        if remaining[result_idx] in marked:

            print(f"Duplicate element is correct, elements in the array are not distinct")
            print(f"Number of calls made to the oracle: {no_of_calls}")

            exit()
    except IndexError:
        print(f"Index out of bound",end=" ")

    except Exception as e:
        raise e
    print(f"Duplicate element is incorrect")
    m = lambda_ * m

print(f"Number of calls made to the oracle: {no_of_calls}")
print("All elements in the array are distinct")