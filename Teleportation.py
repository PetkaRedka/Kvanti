
from qiskit import QuantumCircuit, execute, assemble, Aer, QuantumRegister, ClassicalRegister

# Объявляем симулятор
simulator = Aer.get_backend('statevector_simulator')

# Три регистра: первый - 3 кубита; второй и третий - для 2-х классических битов
qr = QuantumRegister(3)
crz, crx, cr2 = ClassicalRegister(1), ClassicalRegister(1), ClassicalRegister(1)
teleportation_circuit = QuantumCircuit(qr, crz, crx, cr2)

# Пердадим значение 1 от первого кубита третьему
teleportation_circuit.x(0)
teleportation_circuit.barrier()

# Состояние Белла (запутываем второй и третий кубиты).
teleportation_circuit.h(1)
teleportation_circuit.cx(1, 2)
teleportation_circuit.barrier()

# Применяем СNOT для первых 2-х кубитов и оператор Адамара для первого кубита.
teleportation_circuit.cx(0, 1)
teleportation_circuit.h(0)
teleportation_circuit.barrier()

# Измеряем кубиты 0 и 1
teleportation_circuit.measure([0,1], range(2))
teleportation_circuit.barrier()

# В зависимости от результатов измерения применяем 
# операторы I (00), X(01), Z(10) или XZ (11)
teleportation_circuit.z(2).c_if(crz, 1)
teleportation_circuit.x(2).c_if(crx, 1)

# Измерим третий кубит (он должен быть равен 1)
teleportation_circuit.measure(qr[2], 2)

# Проводим симуляцию 1000 раз
# job = execute(teleportation_circuit, simulator, shots=1000)
# result = job.result()
# counts = result.get_counts(teleportation_circuit)

qobj = assemble(teleportation_circuit)
result = simulator.run(qobj).result()
out_state = result.get_statevector()

# Результаты симуляции
# print(counts)
print(out_state)

# Схема
print(teleportation_circuit.draw())