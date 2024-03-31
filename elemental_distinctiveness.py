from qiskit import QuantumCircuit, Aer, transpile, assemble
import numpy as np

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
    """Implement the oracle required for the Grover's algorithm in element distinctness problem"""
    oracle = QuantumCircuit(n)
    oracle.barrier()
    for idx in solution_indices:
        # cnot on binary representation of idx
        control_list=[]
        cl=[]
        target=n-1
        ele=idx
        while(ele>0):
            cl.append(ele%2)
            ele=ele//2
        # cl.reverse()
        # print(cl)
        
        for i in range(len(cl)):
            if(cl[i]==1):
                control_list.append(i)
        
        control_list=[target-1-i for i in control_list]
        # print(idx,"control: ",control_list)
        
        oracle.h(target)
        oracle.mcx(control_list,target) 
        oracle.h(target)

    oracle.barrier()
    # print("oracle circuit:")
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
    qobj = assemble(transpiled_circuit)
    result = qasm_simulator.run(qobj).result()
    counts = result.get_counts()
    # print(counts)

    # Return the most probable state
    return max(counts, key=counts.get)

# Change this to define the array
array=np.random.randint(10, size=10)
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

remaining = array[RootN:]
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
lambda_:int = 2
m:int = 1
for _ in range(int(np.ceil(np.sqrt(N)))):
    k:int = np.random.randint(0, m)
    result = grover_algorithm(logT, k, A_circuit, grover)
    print(f"Duplicate Index returned: {result}")
    result_idx = int(result, 2)
    try:
        if remaining[result_idx] in marked:
            print(f"Duplicate element is correct, elements in the array are not distinct")
            exit()
    except IndexError:
        print(f"Duplicate element is incorrect")
    except Exception as e:
        raise e
    print(f"Duplicate element is incorrect")
    m = lambda_ * m

print("All elements in the array are distinct")