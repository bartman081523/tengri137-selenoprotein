"""Test GPU + ESM + pyDSSP"""
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    # Test GPU operation
    a = torch.randn(100, 100, device='cuda')
    b = torch.randn(100, 100, device='cuda')
    c = a @ b
    print(f"GPU matrix multiply: OK, shape {c.shape}")

# Test ESM
try:
    import esm
    print(f"ESM available: {esm.__version__}")
except ImportError as e:
    print(f"ESM not available: {e}")

# Test pyDSSP
try:
    import pydssp
    print(f"pyDSSP available: {pydssp.__version__}")
except ImportError as e:
    print(f"pyDSSP not available: {e}")
