    
# prepare_simple.py
# Edit data_dir and out_dir then run: python prepare_simple.py

import os, shutil
from glob import glob
import nibabel as nib

# ---------- EDIT THESE ----------
data_dir = r".\ds005602"   # path to your ds005602 folder
out_dir  = r".\prepared_ds"  # output folder (will be created)
# --------------------------------

images_tr = os.path.join(out_dir, "imagesTr")
labels_tr = os.path.join(out_dir, "labelsTr")
os.makedirs(images_tr, exist_ok=True)
os.makedirs(labels_tr, exist_ok=True)

subs = sorted([d for d in os.listdir(data_dir) if d.startswith("sub-") and os.path.isdir(os.path.join(data_dir, d))])
masks_all = sorted(glob(os.path.join(data_dir, "masks", "**", "*.nii*"), recursive=True))

print(f"Found {len(subs)} subjects, {len(masks_all)} masks found in masks/")

for sub in subs:
    anat = os.path.join(data_dir, sub, "anat")
    if not os.path.isdir(anat):
        print(f"[WARN] {sub} has no anat folder, skipping")
        continue

    # try to find T1 and FLAIR inside anat (simple patterns)
    t1 = glob(os.path.join(anat, "*T1*.nii*")) + glob(os.path.join(anat, "*_T1*.nii*")) + glob(os.path.join(anat, "*T1w*.nii*"))
    flair = glob(os.path.join(anat, "*FLAIR*.nii*")) + glob(os.path.join(anat, "*_FLAIR*.nii*")) + glob(os.path.join(anat, "*flair*.nii*"))

    t1p = t1[0] if t1 else None
    fp  = flair[0] if flair else None

    if not t1p and not fp:
        print(f"[WARN] {sub} has no T1 or FLAIR, skipping")
        continue

    # find mask by subject id in masks folder
      # find mask by subject id in masks folder
    mask = None

    # get just the number from "sub-1" → "1"
    sub_num = sub.replace("sub-", "")
    candidates = [sub_num, sub_num.zfill(2), sub_num.zfill(3)]  # e.g. 1, 01, 001

    for m in masks_all:
        bn = os.path.basename(m)
        # match if mask filename starts with or contains the number
        if any(bn.startswith(c) or f"_{c}_" in bn or bn.startswith(f"{c}_") for c in candidates):
            mask = m
            break

    if mask is None:
        print(f"[WARN] No mask found for {sub}, skipping")
        continue
    else:
        print(f"[INFO] Found mask for {sub}: {os.path.basename(mask)}")


    # copy T1 -> _0000, FLAIR -> _0001
    idx = 0
    for src in (t1p, fp):
        if src:
            dst = os.path.join(images_tr, f"{sub}_{idx:04d}.nii.gz")
            try:
                img = nib.load(src)
                nib.save(img, dst)
            except Exception:
                shutil.copy2(src, dst)  # fallback copy
            idx += 1

    # copy mask
    dst_mask = os.path.join(labels_tr, f"{sub}.nii.gz")
    try:
        mimg = nib.load(mask)
        nib.save(mimg, dst_mask)
    except Exception:
        shutil.copy2(mask, dst_mask)

    # quick check: compare shapes of first image and mask
    try:
        img0 = nib.load(os.path.join(images_tr, f"{sub}_0000.nii.gz"))
        lab  = nib.load(dst_mask)
        if img0.shape != lab.shape:
            print(f"[WARN] shape mismatch {sub}: image {img0.shape} vs label {lab.shape}")
    except Exception:
        pass

print("Done. imagesTr and labelsTr ready.")