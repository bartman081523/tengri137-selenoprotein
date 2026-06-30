# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A multi-substrate quantum computing research platform implementing the **Theory of Causal Integrity (TCI)**. Experiments run across three backends simultaneously for cross-validation: x86 software emulator, ESP32-S3 hardware, and IBM Quantum (IBMQ) real hardware.

## Directory Structure

- `ESP32-Causal-Loopback/` — Main project: firmware, Python host scripts, experiment drivers
- `experiments-new-grouped-13778/` — Archived experimental results grouped by discipline

## Build & Flash (ESP32-S3 Firmware)

Uses PlatformIO. From `ESP32-Causal-Loopback/`:

```bash
pio build          # compile firmware
pio upload         # flash to ESP32-S3
pio device monitor # serial monitor at 115200 baud
```

Board: `esp32-s3-devkitc-1`, 16MB flash, Arduino framework.

## Python Environment

```bash
cd ESP32-Causal-Loopback
source venv/bin/activate   # Python 3.14 venv
```

Key scripts:
- `scimind_qpu.py` — Serial controller; opens COM/tty port to ESP32, sends circuits, reads results
- `scimind_engine.py` — SciMind4 core: `UniversalConstants`, `SymbolicOperator`, `GeneratedSymbolicRule`, Wittgenstein Machine
- `scimind_qpu_extensive_test.py` / `scimind_qpu_diagnostics.py` — QPU test suite and diagnostics
- `Experiments_Task_API/batch_test_task_api.py` — API-based experiment orchestration

## Architecture

### Three-Substrate Execution

| Substrate | Speed | Role |
|-----------|-------|------|
| x86 emulator | ~580k shots/sec | Mathematical baseline |
| ESP32-S3 | ~400 shots/sec | Physical hardware emulator |
| IBMQ | varies | Real superconducting qubits |

Results are aggregated and cross-validated. Experiments only count as confirmed when all three substrates agree within tolerances.

### Firmware (`src/main.cpp`)

10-qubit quantum register with a binary opcode protocol (`OP_H`, `OP_CNOT`, `OP_MEASURE`, etc.). Host ↔ device communication is JSON over serial. Dual-core: one core handles quantum ops (mutex-protected), the other handles serial I/O. The v14 firmware adds a **Philosophical Resonance Layer** with RGB LED feedback and FM-modulated audio.

### Python Engine (`scimind_engine.py`)

- `UniversalConstants` — Physical constants (π, e, φ, fine-structure constant α, etc.)
- `SymbolicOperator` — Symbolic algebra tree (unary/binary)
- `GeneratedSymbolicRule` — Template-free rule generation for experiments
- Wittgenstein Machine — Meta-symbolic derivation / Gödel-Turing-style meta-reasoning

### Experiment Data (`experiments-new-grouped-13778/`)

Results are grouped thematically:
- `group1_theoretical_physics/` — 200+ physics experiments (uni_164–uni_286+)
- `group2_machine_learning/` — ML validation
- `group3_p2_5_machine/` — Gödel-Turing-Wittgenstein machine variants
- `group3_psychology/`, `group4_sociology/`, `group5_biology/`, `group6_multiverse/`
- `multi_*/` — Multi-substrate validation batches

## Serial Protocol

Host sends JSON commands; firmware responds with JSON result objects. Each quantum circuit is described as a list of opcodes + arguments. The `scimind_qpu.py` `SciMindQPU` class encapsulates this protocol.

## Key Domain Concepts

- **TCI** — Theory of Causal Integrity: the causality framework all experiments validate against
- **LOCC Teleportation** — Local Operations & Classical Communication protocol implemented on dual cores
- **TOEFI v14** — Transcategorical Spin Experience Framework (Dirac spinors + FM audio modulation)
- **Omega Oracle** — Persistent logging system for protocol sessions (`.jsonl` shot records)
- **Protocol 1018a** — A specific long-running experiment protocol with persistent archival
