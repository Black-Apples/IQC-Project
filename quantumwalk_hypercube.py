from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT

# Add the inverse fourier transform and the fourier transform gates
inv_qft_gate = QFT(4, inverse=True).to_instruction()  
qft_gate = QFT(4, inverse=False).to_instruction()

def get_step_circuit():

    circuit = QuantumCircuit(6, name=' ONE STEP') 
    # Coin operator
    circuit.h([4,5])
    circuit.z([4,5])
    circuit.cz(4,5)
    circuit.h([4,5])

    return circuit

def shift_operator(circuit):
    for i in range(0,4):
        circuit.x(4)
        if i%2==0:
            circuit.x(5)
        circuit.ccx(4,5,i)

def phase_oracle_hardcoded():

    circuit =  QuantumCircuit(6)

    # Mark 1011
    circuit.x(2)
    circuit.h(3)
    circuit.mcx([0,1,2], 3)
    circuit.h(3)
    circuit.x(2)

    # Mark 1111
    circuit.h(3)
    circuit.mcx([0,1,2],3)
    circuit.h(3)

    return circuit.to_instruction()

def get_phase_estimation_gate(cont_one_step, inv_cont_one_step, mark_auxiliary_gate):
    # Phase estimation
    circuit = QuantumCircuit(11)
    circuit.h([0,1,2,3])
    for i in range(0,4):
        stop = 1<<i
        for j in range(0,stop):
            circuit.append(cont_one_step, [i,4,5,6,7,8,9])

    # Inverse fourier transform
    circuit.append(inv_qft_gate, [0,1,2,3])

    # Mark all angles theta that are not 0 with an auxiliary qubit
    circuit.append(mark_auxiliary_gate, [0,1,2,3,10])

    # Reverse phase estimation
    circuit.append(qft_gate, [0,1,2,3])   

    for i in range(3,-1,-1):
        stop = 1<<i
        for j in range(0,stop):
            circuit.append(inv_cont_one_step, [i,4,5,6,7,8,9])
    circuit.barrier(range(0,10))
    circuit.h([0,1,2,3])

    return circuit.to_instruction()   


def get_auxillary_marking_gate():

    circuit = QuantumCircuit(5)
    circuit.x([0,1,2,3,4])
    circuit.mcx([0,1,2,3], 4)
    circuit.z(4)
    circuit.mcx([0,1,2,3], 4)
    circuit.x([0,1,2,3,4])

    return circuit.to_instruction()

# Adding the circuit for one step of the quantum walk
one_step_circuit = get_step_circuit()
shift_operator(one_step_circuit)

# Make controlled versions of the one step circuit
inv_cont_one_step = one_step_circuit.inverse().control()
cont_one_step = one_step_circuit.control()

phase_oracle_gate = phase_oracle_hardcoded()
mark_auxiliary_gate = get_auxillary_marking_gate()
phase_estimation_gate = get_phase_estimation_gate(cont_one_step, inv_cont_one_step, mark_auxiliary_gate)

# Implementation of the full quantum walk search algorithm
theta_q = QuantumRegister(4, 'theta')
node_q = QuantumRegister(4, 'node')
coin_q = QuantumRegister(2, 'coin')
auxiliary_q = QuantumRegister(1, 'auxiliary')
creg = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(theta_q, node_q, coin_q, auxiliary_q, creg)
# Apply Hadamard gates to the qubits that represent the nodes and the coin
circuit.h([4,5,6,7,8,9])
# Hardcoding the required number of iterations
iterations = 2

for i in range(0,iterations):
    circuit.append(phase_oracle_gate, [4,5,6,7,8,9])
    circuit.append(phase_estimation_gate, [0,1,2,3,4,5,6,7,8,9,10])

circuit.measure(node_q[0], creg[0])
circuit.measure(node_q[1], creg[1])
circuit.measure(node_q[2], creg[2])
circuit.measure(node_q[3], creg[3])

# Execute the circuit
backend = Aer.get_backend('qasm_simulator') 
job = execute( circuit, backend, shots=1000) 
res = job.result().get_counts() 
print(res)