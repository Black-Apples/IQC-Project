import warnings
import numpy as np
from tqdm import tqdm
from qiskit import QuantumCircuit, Aer, transpile, assemble
# suppress the warnings
warnings.filterwarnings("ignore")

ARRAY_SIZE:int = 100
MAX_ELEMENT:int = ARRAY_SIZE # As per the problem statement in the paper
NUM_SHOTS:int = 1
TEST_ITERATIONS:int = 100

def grover_iterator(oracle_circuit,idx_qubits,qubits)->QuantumCircuit:
    """Implement the Grover's iterator to solve the problem"""
    qc=QuantumCircuit(qubits)
    qc.append(oracle_circuit,range(qubits))
    # qc.barrier()
    qc.h(range(idx_qubits))
    qc.h(qubits-1)
    qc.x(range(idx_qubits))
    qc.x(qubits-1)
    qc.barrier()
    qc.h(qubits-1)
    qc.mcx(list(range(idx_qubits)),qubits-1)
    qc.h(qubits-1)
    qc.barrier()
    qc.x(qubits-1)
    qc.x(range(idx_qubits))
    qc.h(qubits-1)
    qc.h(range(idx_qubits))
    qc.barrier()
    return qc

def A(idx_qubits,qubits)->QuantumCircuit:
    """Implement the A operator for generating the superposition of all states"""
    qc = QuantumCircuit(qubits)
    for qubit in range(idx_qubits):
        qc.h(qubit)
    qc.h(qubits-1)
    qc.barrier()
    return qc

def Array_oracle(idx_qubits,oracle_qubits,Array)->QuantumCircuit:
    """Implement the oracle for the obtaining the elements of the array using the index"""
    oracle = QuantumCircuit(idx_qubits+oracle_qubits)
    array_len = len(Array)
    idx=[i for i in range(2**idx_qubits)]
    oracle.barrier()
    for element in idx:
        # Convert idx to binary representation
        binary_rep_idx = bin(element)[2:].zfill(idx_qubits)
        # print(binary_rep_idx)

        # reverse the binary representation
        binary_rep_idx = binary_rep_idx[::-1]

        # Apply X gates on qubits where binary_rep is '1'
        for i, bit in enumerate(binary_rep_idx):
            if bit == '0':
                oracle.x(i)

        # Apply multi-controlled X gate to create elements of array
        if(element>=array_len):
            number=0
        else:
            number=Array[element]
        binary_rep_number = bin(number)[2:].zfill(oracle_qubits)
        binary_rep_number = binary_rep_number[::-1]
        # print(binary_rep_number,number,binary_rep_idx,element)
        # print(binary_rep_number)
        for i, bit in enumerate(binary_rep_number):
            if bit == '1':
                oracle.mcx(list(range(0,idx_qubits)), idx_qubits+i)
        # oracle.mcx(list(range(0,idx_qubits)), idx_qubits+1)

        # Unapply X gates
        for i, bit in enumerate(binary_rep_idx):
            if bit == '0':
                oracle.x(i)
        
        oracle.barrier()

    oracle.barrier()
    # print("Array Oracle circuit:")
    # print(oracle)
    return oracle

def comparision_oracle(idx_qubits, oracale_qubits,marked_elements):
    oracle = QuantumCircuit(idx_qubits+oracale_qubits)

    oracle.barrier()
    for element in marked_elements:
        # Convert idx to binary representation
        binary_rep = bin(element)[2:].zfill(oracale_qubits-1)
        
        # print(binary_rep)
        # reverse the binary representation
        binary_rep = binary_rep[::-1]
        # Apply X gates on qubits where binary_rep is '1'
        for i, bit in enumerate(binary_rep):
            if bit == '0':
                oracle.x(i+idx_qubits)

        # Apply multi-controlled X gate
        oracle.h(oracale_qubits-1+idx_qubits)
        oracle.mcx(list(range(0+idx_qubits,oracale_qubits-1+idx_qubits)), oracale_qubits-1+idx_qubits)
        oracle.h(oracale_qubits-1+idx_qubits)
        # Unapply X gates
        for i, bit in enumerate(binary_rep):
            if bit == '0':
                oracle.x(i+idx_qubits)
        
        oracle.barrier()

    oracle.barrier()
    # print("Compasion Oracle circuit:")
    # print(oracle)
    return oracle

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

def grover_algorithm(qubits, idx_qubits, k, A_circuit, grover_circuit):
    """Implement the Grover's algorithm for element distinctness problem"""
    # Creating the main circuit
    circuit=QuantumCircuit(qubits, idx_qubits)
    # Adding the A operator to create the superposition of all states before passing to Grover's iterator
    circuit.append(A_circuit, range(qubits))
    # Adding the Grover's iterator
    for _ in range(k):
        circuit.append(grover_circuit, range(qubits))

    # measurement
    circuit.measure(range(idx_qubits), range(idx_qubits))

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

def element_distinctness_quantum(array)->(bool, int):
    """Check for the duplicates in the array using Grover's algorithm for element distinctness problem"""
    # print("Running the test for the element distinctness problem")
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
    idx_qubits:int = int(np.ceil(np.log2(T)))
    element_qubits:int = int(np.ceil(np.log2(MAX_ELEMENT)))
    oracle_qubits:int = element_qubits
    qubits:int = idx_qubits + oracle_qubits

    # Creating individual circuits
    array_circuit:QuantumCircuit = Array_oracle(idx_qubits, oracle_qubits, remaining)
    comparision_circuit:QuantumCircuit = comparision_oracle(idx_qubits, oracle_qubits, marked)
    oracle_circuit:QuantumCircuit = QuantumCircuit(qubits)
    oracle_circuit.append(array_circuit, range(qubits))
    oracle_circuit.append(comparision_circuit, range(qubits))
    oracle_circuit.append(array_circuit, range(qubits))
    
    A_circuit:QuantumCircuit = A(idx_qubits, qubits)
    grover:QuantumCircuit = grover_iterator(oracle_circuit, idx_qubits, qubits)

    # Running the Grover's algorithm for unknown theta
    lambda_:int = 1.2
    m:int = 2
    no_of_loops:int = 0
    for _ in range(int(np.ceil(np.sqrt(N)))):
        no_of_loops += 1
        k:int = np.random.randint(1, m)
        no_of_calls += k*NUM_SHOTS
        result = grover_algorithm(qubits, idx_qubits, k, A_circuit, grover)
        # print(f"Duplicate Index returned: {result}")
        result_idx = int(result, 2)
        try:
            # print(f"Duplicate element: {remaining[result_idx]}")
            if remaining[result_idx] in marked:

                # print(f"Duplicate element is correct, elements in the array are not distinct")
                # print(f"Number of calls made to the oracle: {no_of_calls}")
                return False, no_of_calls
                
        except IndexError:
            # print(f"Index out of bound",end=" ")
            pass

        except Exception as e:
            raise e
        # print(f"Duplicate element is incorrect")
        m = lambda_ * m

    return True, no_of_calls

def element_distinctness_classical(array:list[int])->bool:
    """Checks for duplicates in the array using classical approach"""
    if len(array) == len(set(array)):
        return True
    return False

def simulate_test()->(bool, int):
    """Simulate the test for element distinctness problem"""
    array=np.random.randint(MAX_ELEMENT, size=ARRAY_SIZE)
    tot_calls:int = 0
    res:bool = False
    # Run the Grover's algorithm N^0.25 times to minimize the error probability
    for _ in range(int(np.ceil(np.power(ARRAY_SIZE, 0.25)))):
        res, calls = element_distinctness_quantum(array)
        tot_calls += calls
        if res:
            break
    # Confirm the result using classical approach
    actual_res:bool = element_distinctness_classical(array)
    return res == actual_res, tot_calls

if __name__ == "__main__":
    num_calls:list[int] = []
    error_cnt:int = 0
    for _ in tqdm(range(TEST_ITERATIONS), desc="Running test iterations"):
        result, calls = simulate_test()
        num_calls.append(calls)
        if not result:
            error_cnt += 1

    print(f"Fraction of incorrect classifications: {error_cnt/TEST_ITERATIONS}")
    print(f"Average number of calls made to the oracle: {np.mean(num_calls)}")
    