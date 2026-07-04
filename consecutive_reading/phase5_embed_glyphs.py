#!/usr/bin/env python3
"""
Phase 5 v4 — Multi-Resolution-Glyph-Embeddings.

Input:
  - bbox/components_20260704_V4/p{NN}/p{NN}_glyphs.json  (Phase 2 v4 Glyphen)
  - bbox/components_20260704_V4/p{NN}/p{NN}_glyphs/g*.png  (Glyph-Crops)
  - models/symbols_20260704_V2/model.pt  (V2-Warm-Start, 32x32 EmbeddingNet)

Output:
  - bbox/embeddings_20260704_V4/crop_embeddings.npz
    {
      "embeddings": [N, 192],  # 16+32+64 concatenation
      "embeddings_16": [N, 64],
      "embeddings_32": [N, 64],
      "embeddings_64": [N, 64],
      "glyph_index": [N],
      "page_id": [N],
      "bbox": [N, 4],
      "size_px": [N],
      "fill_ratio": [N],
      "n_components": [N],
      "type_hint": [N]
    }

Algorithmus:
1. Lade V2 EmbeddingNet (32x32, 64-dim, V2-Warm-Start)
2. Pro Glyph: berechne 3 Embeddings (16+32+64 px Inputs) → 192-dim
3. Multi-Resolution-Head:
   - 16x16 Branch: Pad/Resize auf 16x16, dann durch V2-Netz
   - 32x32 Branch: V2-Default
   - 64x64 Branch: Pad/Resize auf 64x64, dann durch V2-Netz
4. L2-Normalisierung pro Branch
5. Konkatenation → 192-dim
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "models" / "symbols_20260704_V2"))
from inference import EmbeddingNet, preprocess  # noqa: E402

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def preprocess_at_size(path: Path, size: int) -> torch.Tensor:
    """Pad auf Square + Resize auf (size, size) + Normalisierung.
    Output shape: (1, size, size) — 3D, wie V2-inference.preprocess().
    Der Aufrufer macht .unsqueeze(0) → (1, 1, size, size)."""
    img = Image.open(path).convert("L")
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    a = (a - 0.5) / 0.5
    return torch.from_numpy(a).unsqueeze(0)


def l2_normalize(x: torch.Tensor) -> torch.Tensor:
    """L2-normalize along last dim."""
    return x / x.norm(dim=-1, keepdim=True).clamp(min=1e-8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_<TS>/")
    ap.add_argument("--model", type=Path, required=True,
                    help="V2 model.pt (Warm-Start)")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/embeddings_<TS>/")
    ap.add_argument("--device", default="cpu",
                    help="cpu oder cuda")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    device = torch.device(args.device)
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model, map_location="cpu", weights_only=True))
    model.eval()
    model.to(device)
    print(f"Loaded V2 model from {args.model}")

    # Sammle alle Glyphen über alle Pages
    all_glyphs = []
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        glyphs_path = args.components / page_id / f"{page_id}_glyphs.json"
        if not glyphs_path.exists():
            continue
        gd = json.loads(glyphs_path.read_text())
        for g in gd.get("glyphs", []):
            all_glyphs.append(g)
    print(f"Total glyphs: {len(all_glyphs)}")

    # Compute embeddings at 3 resolutions
    embs_16 = np.zeros((len(all_glyphs), 64), dtype=np.float32)
    embs_32 = np.zeros((len(all_glyphs), 64), dtype=np.float32)
    embs_64 = np.zeros((len(all_glyphs), 64), dtype=np.float32)
    glyph_index = []
    page_id_arr = []
    bbox_arr = []
    size_px_arr = []
    fill_ratio_arr = []
    n_components_arr = []
    type_hint_arr = []

    for idx, g in enumerate(all_glyphs):
        crop_path = ROOT / g["crop_path"] if g.get("crop_path") else None
        if not crop_path or not crop_path.exists():
            continue
        try:
            with torch.no_grad():
                # preprocess_at_size returns 3D (1, H, W); model expects 4D (1, 1, H, W)
                x16 = preprocess_at_size(crop_path, 16).unsqueeze(0).to(device)
                x32 = preprocess_at_size(crop_path, 32).unsqueeze(0).to(device)
                x64 = preprocess_at_size(crop_path, 64).unsqueeze(0).to(device)
                e16 = l2_normalize(model(x16)).cpu().numpy().squeeze()
                e32 = l2_normalize(model(x32)).cpu().numpy().squeeze()
                e64 = l2_normalize(model(x64)).cpu().numpy().squeeze()
            embs_16[idx] = e16
            embs_32[idx] = e32
            embs_64[idx] = e64
        except Exception as e:
            print(f"  Embedding failed for glyph {g['glyph_index']}: {e}")
            continue
        glyph_index.append(g["glyph_index"])
        page_id_arr.append(g["page"])
        bbox_arr.append(g["bbox"])
        size_px_arr.append(g.get("size_px", 0))
        fill_ratio_arr.append(g.get("fill_ratio", 0.0))
        n_components_arr.append(g.get("n_components", 0))
        type_hint_arr.append(g.get("type_hint", "unknown"))
        if (idx + 1) % 100 == 0:
            print(f"  {idx + 1}/{len(all_glyphs)} glyphs embedded")

    # Filter out the zero-entries (failed)
    n_ok = len(glyph_index)
    print(f"Successfully embedded: {n_ok} / {len(all_glyphs)}")

    # Concatenate
    embeddings = np.concatenate([embs_16[:n_ok], embs_32[:n_ok], embs_64[:n_ok]], axis=1)

    np.savez_compressed(
        args.out / "crop_embeddings.npz",
        embeddings=embeddings,
        embeddings_16=embs_16[:n_ok],
        embeddings_32=embs_32[:n_ok],
        embeddings_64=embs_64[:n_ok],
        glyph_index=np.array(glyph_index, dtype=np.int32),
        page_id=np.array(page_id_arr),
        bbox=np.array(bbox_arr, dtype=np.int32),
        size_px=np.array(size_px_arr, dtype=np.int32),
        fill_ratio=np.array(fill_ratio_arr, dtype=np.float32),
        n_components=np.array(n_components_arr, dtype=np.int32),
        type_hint=np.array(type_hint_arr),
    )
    print(f"Saved embeddings to {args.out / 'crop_embeddings.npz'}")
    print(f"Shape: {embeddings.shape}")


if __name__ == "__main__":
    main()
