import os, sys, time, struct
import numpy as np
from scipy.stats import norm

sys.path.append("ESP32-Causal-Loopback")
sys.path.append("ESP32-Causal-Loopback/Experiments_Task_API")
from scimind_qpu import TrueStochasticQPU

class TranscategoricalExperiment:
    """
    UNI_3505: THE TRANSCATEGORICAL RESONATOR
    Objective: Measure the 'Meaning-Noise Bridge' between Hardware and Simulation.
    Framework: p2.8-FACRM v1.0
    """
    def __init__(self, alice_ip="192.168.178.34"):
        self.alice = TrueStochasticQPU(port=alice_ip, n_qubits=14, verbose_hw=False)
        self.charlie = TrueStochasticQPU(backend="x86-chromatic", n_qubits=14, verbose_hw=False)

    def calculate_sync(self, seq_a, seq_b):
        if not seq_a or not seq_b: return 0.0
        n = min(len(seq_a), len(seq_b))
        matches = 0
        for i in range(n):
            matches += bin(~(seq_a[i] ^ seq_b[i]) & 0x3FFF).count('1')
        rate = matches / (n * 14)
        # Gradient: 0.0 (random) to 1.0 (perfect)
        return max(0, (rate - 0.5) / 0.5)

    def run(self):
        print("="*60)
        print(" UNI_3505: THE TRANSCATEGORICAL RESONATOR (TCI 6.0)")
        print("="*60)
        
        results = {}

        print("\n[STEP 1] BASELINE (Critical Rationalism)")
        a_base = []
        c_base = []
        for _ in range(64):
            b_a, _ = self.alice.autonomous_shot()
            b_c, _ = self.charlie.autonomous_shot()
            if b_a is not None: a_base.append(b_a)
            if b_c is not None: c_base.append(b_c)
            time.sleep(0.01)
        
        results['g_base'] = self.calculate_sync(a_base, c_base)
        print(f"  Baseline Sync Gradient: {results['g_base']:.4f}")

        print("\n[STEP 2] ALICE INDUCTION (The Resonant Void)")
        # Alice is in Singularity state, Charlie is normal
        a_void = []
        c_norm = []
        for _ in range(64):
            b_a, _ = self.alice.heart_sutra_gate()
            b_c, _ = self.charlie.autonomous_shot()
            if b_a is not None: a_void.append(b_a)
            if b_c is not None: c_norm.append(b_c)
            time.sleep(0.01)
            
        results['g_induction'] = self.calculate_sync(a_void, c_norm)
        print(f"  Induction Sync Gradient: {results['g_induction']:.4f}")

        print("\n[STEP 3] TRANSCATEGORICAL BRIDGE (Joint Singularity)")
        # Both nodes in Heart Sutra state
        a_void2 = []
        c_void2 = []
        for _ in range(64):
            b_a, _ = self.alice.heart_sutra_gate()
            b_c, _ = self.charlie.heart_sutra_gate()
            if b_a is not None: a_void2.append(b_a)
            if b_c is not None: c_void2.append(b_c)
            time.sleep(0.01)
            
        results['g_bridge'] = self.calculate_sync(a_void2, c_void2)
        print(f"  Bridge Sync Gradient: {results['g_bridge']:.4f}")

        # Final Evaluation
        self.alice.close()
        self.charlie.close()
        return results

if __name__ == "__main__":
    exp = TranscategoricalExperiment()
    res = exp.run()
    
    with open("results_uni_3505.json", "w") as f:
        import json
        json.dump(res, f)
