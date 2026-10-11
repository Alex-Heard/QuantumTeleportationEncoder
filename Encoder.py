from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import json

simulator = AerSimulator()

state = input("Type '1' to encode and '2' to decode:")

if state == '1':
    user_str = input("Please enter a string to encode: ")
    binary_result = ''.join(format(ord(char), '08b') for char in user_str)

    statevectors = []
    keystring = ""

    for bit in binary_result:
        qc = QuantumCircuit(3,2)
        qc.h(1)
        qc.cx(1,2)
        if bit == '1':
            qc.x(0)
        qc.cx(0,1)
        qc.h(0)
        qc.measure(0,0)
        qc.measure(1,1)

        qc.save_statevector()

        result = simulator.run(qc, shots=1).result()
        sv = result.get_statevector()
        statevectors.append(sv)

        measured_bits = list(result.get_counts().keys())[0]
        keystring += measured_bits

    print(f"Keystring: {keystring}")


    serializable_statevectors = []

    for sv in statevectors:
        formatted_vector = [[amplitude.real, amplitude.imag] for amplitude in sv.data]
        serializable_statevectors.append(formatted_vector)

    with open("statevectors.json", "w") as json_file:
        json.dump(serializable_statevectors, json_file, indent=4)
    
    print("Statevectors successfully saved to statevectors.json!")

elif state == '2':
    with open("statevectors.json", "r") as json_file:
        loaded_data = json.load(json_file)

    rebuilt_statevectors = [
        [complex(real, imag) for real, imag in vector] 
        for vector in loaded_data
    ]

    keystring = input(f"Keystring: ")

    decoded_binary = ""

    for i, sv in enumerate(rebuilt_statevectors):
        bits = keystring[i*2 : i*2+2]
        c1 = bits[0] 
        c0 = bits[1]
        qc = QuantumCircuit(3, 1)
        qc.initialize(sv, [0, 1, 2])

        if c1 == '1':
            qc.x(2)

        if c0 == '1':
            qc.z(2)

        qc.measure(2, 0)
        result = simulator.run(qc, shots=1).result()
        
        measured_bit = list(result.get_counts().keys())[0]
        decoded_binary += measured_bit

    decoded_message = ''.join(
        chr(int(decoded_binary[i:i+8], 2)) 
        for i in range(0, len(decoded_binary), 8)
    )

    print(f"Decoded Message: {decoded_message}")