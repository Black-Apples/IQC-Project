from qiskit import QuantumCircuit, Aer, transpile, assemble
import numpy as np
import warnings
from tqdm import tqdm
# suppress the warnings
warnings.filterwarnings("ignore")

ARRAY_SIZE:int = 100
NUM_SHOTS:int = 1
TEST_ITERATIONS:int = 1000

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

def oracle(n, solution_indices)->QuantumCircuit:
    """Implement the oracle for the element distinctness problem"""
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
    qobj = assemble(transpiled_circuit, shots=NUM_SHOTS)
    result = qasm_simulator.run(qobj).result()
    counts = result.get_counts()
    # print(counts)

    # Return the most probable state
    return max(counts, key=counts.get)

def simulate_test()->(bool, int):
    """Simulate the test for the element distinctness problem"""
    # print("Running the test for the element distinctness problem")
    array=np.random.randint(ARRAY_SIZE**2, size=ARRAY_SIZE)
    N:int = len(array)
    np.random.shuffle(array)
    # print(f"Initial Array: {array}")

    # Pick random sqrt(N) elements
    RootN:int = int(np.sqrt(N))
    marked = array[:RootN]
    no_of_calls:int = RootN
    # print(f"Marked elements: {marked}")
    if(len(set(marked))!=len(marked)):
        # print("Marked elements are not unique, found duplicates")
        return False, no_of_calls

    # Adding a dummy element to index 0
    remaining = array[RootN:]
    # print(f"Remaining elements: {remaining}")
    T:int = len(remaining)
    logT:int = int(np.ceil(np.log2(T)))

    # Creating the oracle using the dupicates
    solution_idx:list[int] = []
    for i in marked:
        for j in range(len(remaining)):
            if i==remaining[j]:
                solution_idx.append(j)
    oracle_circuit:QuantumCircuit = oracle(logT+1, solution_idx)

    grover:QuantumCircuit = grover_iterator(oracle_circuit,logT+1)
    A_circuit:QuantumCircuit = A(logT+1)

    # Running the Grover's algorithm for unknown theta
    lambda_:int = 1.2
    m:int = 2
    for _ in range(int(np.ceil(np.sqrt(N)))):
        k:int = np.random.randint(1, m)
        no_of_calls+=k
        result = grover_algorithm(logT, k, A_circuit, grover)
        # print(f"Duplicate Index returned: {result}")
        result_idx = int(result, 2)
        try:
            # print(f"Duplicate element: {remaining[result_idx]}")
            if remaining[result_idx] in marked:

                # print(f"Duplicate element is correct, elements in the array are not distinct")
                # print(f"Number of calls made to the oracle: {no_of_calls}")
                return True, no_of_calls
                
        except IndexError:
            # print(f"Index out of bound",end=" ")
            pass

        except Exception as e:
            raise e
        # print(f"Duplicate element is incorrect")
        m = lambda_ * m

    return False, no_of_calls

if __name__ == "__main__":
    num_calls:list[int] = []
    for _ in tqdm(range(TEST_ITERATIONS), desc="Running test iterations"):
        result, calls = simulate_test()
        num_calls.append(calls)
    print(f"Average number of calls made to the oracle: {np.mean(num_calls)}")
    #  n**3/4
    print(f"Expected number of calls made to the oracle: {ARRAY_SIZE**(3/4)}")