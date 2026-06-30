# Experiment ID: uni-185
# Version Index: 13

import numpy as np
import matplotlib.pyplot as plt
import scipy.fft
import sys
import os

# ==============================================================================
# LOGGER SETUP
# ==============================================================================

class GeneticSystem:
    def __init__(self, target_shape_size=64):
        self.size = target_shape_size
        # Ziel: Ein "X" Form (Komplex genug, um Struktur zu prüfen)
        self.target = np.zeros((self.size, self.size))
        for i in range(10, self.size-10):
            self.target[i, i] = 1.0
            self.target[i, self.size-i-1] = 1.0
        
        self.genome = None
        self.phenotype = None

    def encode(self):
        raise NotImplementedError

    def decode(self, genome):
        raise NotImplementedError

    def mutate(self, rate=0.1, delete_chunk=False):
        """Simuliert DNA-Schäden: Rauschen und massiver Informationsverlust."""
        if self.genome is None: return None
        
        # 1. Rauschen (Punktmutationen)
        noise = np.random.normal(0, rate, self.genome.shape)
        mutated_genome = self.genome + noise
        
        # 2. Deletion (Strangbruch - Lösche einen ganzen Block)
        if delete_chunk:
            flat = mutated_genome.flatten()
            L = len(flat)
            # Lösche 30% des Codes am Stück (katastrophaler Schaden)
            start = np.random.randint(0, int(L*0.7))
            end = start + int(L*0.3)
            flat[start:end] = 0 # Information destroyed (Gap)
            mutated_genome = flat.reshape(self.genome.shape)
            
        return mutated_genome

    def get_fitness(self, phenotype):
        # MSE zum Target (Niedriger Fehler = Hohe Fitness)
        # Normalisieren für fairen Vergleich (Helligkeit ist egal, Struktur zählt)
        p_min, p_max = np.min(phenotype), np.max(phenotype)
        if p_max - p_min < 1e-9:
             p_norm = phenotype
        else:
             p_norm = (phenotype - p_min) / (p_max - p_min)
             
        mse = np.mean((p_norm - self.target)**2)
        return 1.0 - mse # Score (Max 1.0)

# --- MODELL A: INSTRUKTION (Seriell / Vektor) ---
class InstructionalSystem(GeneticSystem):
    def encode(self):
        # Wir speichern die Koordinaten der aktiven Pixel
        points = np.argwhere(self.target > 0.5)
        # Genom ist eine Liste von (x, y) Koordinaten
        self.genome = points.astype(float)
        
    def decode(self, genome):
        grid = np.zeros((self.size, self.size))
        # Interpreter
        # Da das Genom mutiert ist, sind Werte nun floats und können NaN/0 sein
        flat_genome = genome.flatten()
        # Reshape zurück zu Paaren, falls möglich, oder interpretiere als Stream
        # Einfachheit: Wir nehmen an, Struktur (N, 2) bleibt erhalten, aber Werte sind kaputt
        
        try:
            points = genome.reshape(-1, 2)
            for p in points:
                # Round to nearest pixel
                if np.isnan(p).any(): continue
                x = int(round(p[0]))
                y = int(round(p[1]))
                if 0 <= x < self.size and 0 <= y < self.size:
                    grid[x, y] = 1.0
        except:
            pass # Genom zerstört
        return grid

# --- MODELL B: ENERGIE (Lokal / Bitmap) ---
class EnergeticSystem(GeneticSystem):
    def encode(self):
        # Genom = Das Bild selbst (1:1 Mapping)
        self.genome = self.target.copy()
        
    def decode(self, genome):
        # Direkte Projektion
        return genome

# --- MODELL C: HOLOGRAPHISCH (Verteilt / Frequenz) ---
class HolographicSystem(GeneticSystem):
    def encode(self):
        # Genom ist die Fourier-Transformierte (Spektrum)
        # Jeder Punkt im Genom (Frequenz) trägt zum GANZEN Bild bei.
        ft = scipy.fft.fft2(self.target)
        # Wir speichern Real- und Imaginärteil getrennt
        self.genome = np.stack([ft.real, ft.imag])
        
    def decode(self, genome):
        # Rekonstruktion aus Frequenzen
        # Auch wenn Frequenzen fehlen (Deletion), bleibt das Bild erhalten (nur unschärfer)
        if genome.shape[0] != 2: return np.zeros((self.size, self.size))
        
        ft_rec = genome[0] + 1j * genome[1]
        recon = scipy.fft.ifft2(ft_rec).real
        return recon

def run_experiment():
    print("="*80)
    print("FACRM EXPERIMENT UNI-185: THE MUTATION RESILIENCE TEST")
    print("Hypothese: Informationskodierung bestimmt Robustheit.")
    print("="*80)

    systems = {
        "A (Instructional)": InstructionalSystem(),
        "B (Energetic/Map)": EnergeticSystem(),
        "C (Holographic)": HolographicSystem()
    }

    # 1. Encoding (Perfekte Welt)
    print("\n[PHASE 1] Encoding & Baseline Check...")
    for name, sys in systems.items():
        sys.encode()
        # Test Perfect Recall
        pheno = sys.decode(sys.genome)
        fit = sys.get_fitness(pheno)
        print(f"   {name} Baseline Fitness: {fit:.4f}")

    # 2. Stress Test (Massive Zerstörung)
    print("\n[PHASE 2] Stress Test (Noise + 30% Deletion)...")
    results = {}
    phenotypes = {}
    
    for name, sys in systems.items():
        # Mutierte DNA erzeugen
        mutated_dna = sys.mutate(rate=2.0, delete_chunk=True) # Hohes Rauschen
        
        # Phänotyp ausbilden
        pheno = sys.decode(mutated_dna)
        
        # Fitness messen
        fit = sys.get_fitness(pheno)
        results[name] = fit
        phenotypes[name] = pheno
        print(f"   {name} Stressed Fitness: {fit:.4f}")

    # --- SYNTHESE & PLOTTING ---
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    # Target anzeigen
    axes[0].imshow(systems["A (Instructional)"].target, cmap='gray')
    axes[0].set_title("TARGET FORM (Original)")
    axes[0].axis('off')
    
    # Gewinner ermitteln
    winner = max(results, key=results.get)
    
    # Ergebnisse anzeigen
    for i, (name, img) in enumerate(phenotypes.items()):
        # Normalize for display clarity
        p_min, p_max = np.min(img), np.max(img)
        if p_max - p_min > 0:
            img_norm = (img - p_min) / (p_max - p_min)
        else:
            img_norm = img
            
        axes[i+1].imshow(img_norm, cmap='viridis')
        title_color = 'green' if name == winner else 'black'
        axes[i+1].set_title(f"{name}\nFit: {results[name]:.4f}", color=title_color, fontweight='bold')
        axes[i+1].axis('off')

    plt.tight_layout()
    plt.savefig("185_genetic_resilience.png")
    print(f"[INFO] Plot saved: 185_genetic_resilience.png")
    print("\n[INFO] Plot '185_genetic_resilience.png' gespeichert.")

    # AUTOMATED SYNTHESIS ENGINE
    print("\n" + "="*80)
    print("FACRM SYNTHESIS ENGINE")
    print("="*80)
    print(f"Gewinner der Resilienz: {winner}")
    
    next_vector = ""
    
    if "Instructional" in winner:
        print(">> INTERPRETATION: Serialität ist robust. DNA ist eine Liste.")
        print(">> FALSIFIKATION TCI: Holographie ist unnötig kompliziert.")
        next_vector = "FOCUS_ALGORITHMIC_BIO"
        
    elif "Energetic" in winner:
        print(">> INTERPRETATION: Direkte Abbildung (Lokalität) gewinnt.")
        print(">> Ein Loch im Genom ist ein Loch im Körper. Keine 'Geister'.")
        next_vector = "FOCUS_LOCAL_PHYSICS"
        
    elif "Holographic" in winner:
        print(">> INTERPRETATION: Verteilte Information überlebt lokale Zerstörung.")
        print(">> KORROBORATION TCI: Das Ganze ist in jedem Teil enthalten.")
        print("   Wenn man 30% des Hologramms löscht, wird das Bild nur unschärfer,")
        print("   aber die Form (das 'X') bleibt erhalten.")
        next_vector = "FOCUS_QUANTUM_GENETICS"
        
    print(f"\n>> STRATEGIC VECTOR FOR NEXT SESSION: {next_vector}")
    return next_vector

if __name__ == "__main__":
    vector = run_experiment()
    # Write vector to file for Meta-Analysis
    with open("strategic_vector_185.txt", "w") as f:
        f.write(vector)
