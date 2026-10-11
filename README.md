# Quantum Teleportation Text Encoder

This project implements a quantum teleportation protocol to encode and decode text messages using Qiskit's `AerSimulator`. It translates standard text strings into binary, prepares the corresponding quantum states, and teleports them across a simulated 3-qubit circuit.

## How It Works

The teleportation protocol splits the message information into two distinct components:
1. **The Quantum State:** The statevectors of the teleported qubits are serialized and saved locally to a file named `statevectors.json`.
2. **The Classical Keystring:** A sequence of classical bits generated via Bell-state measurements (using CNOT and Hadamard gates) during the encoding process.

To decode the message, the receiver must possess both the `statevectors.json` file and the exact classical keystring to apply the correct conditional X and Z correction gates.

## Prerequisites

To run this script, you will need Python installed along with the Qiskit libraries.

```bash
pip install qiskit qiskit-aer
