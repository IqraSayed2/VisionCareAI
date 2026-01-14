import os
import shutil
import random
import zipfile

def copy_images(src, dst, limit):
    if not os.path.exists(src):
        print(f"Source {src} does not exist")
        return
    images = os.listdir(src)
    print(f"Source {src} has {len(images)} images")
    random.shuffle(images)
    images = images[:limit]

    os.makedirs(dst, exist_ok=True)

    for img in images:
        shutil.copy(os.path.join(src, img), os.path.join(dst, img))
    print(f"Copied {len(images)} images to {dst}")


# ---------- PATHS (CHANGE ONLY ROOT FOLDERS) ----------

DR_PATH = r"C:/Users/RENTKAR/Downloads/archive (3)/colored_images"
GLAUCOMA_PATH = r"C:/Users/RENTKAR/Downloads/archive (1)/RIM-ONE_DL_images/partitioned_randomly"
CATARACT_PATH = r"C:/Users/RENTKAR/Downloads/archive (2)/processed_images"

# Extract zips if they exist
dr_zip = r"C:/Users/RENTKAR/Downloads/archive (3).zip"
if os.path.exists(dr_zip):
    with zipfile.ZipFile(dr_zip, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(DR_PATH))

glaucoma_zip = r"C:/Users/RENTKAR/Downloads/archive (1).zip"
if os.path.exists(glaucoma_zip):
    with zipfile.ZipFile(glaucoma_zip, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(os.path.dirname(GLAUCOMA_PATH)))
    print(f"Extracted {glaucoma_zip} to {os.path.dirname(os.path.dirname(GLAUCOMA_PATH))}")
    print("Contents:", os.listdir(os.path.dirname(os.path.dirname(GLAUCOMA_PATH))))

cataract_zip = r"C:/Users/RENTKAR/Downloads/archive (2).zip"
if os.path.exists(cataract_zip):
    with zipfile.ZipFile(cataract_zip, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(CATARACT_PATH))
    print(f"Extracted {cataract_zip} to {os.path.dirname(CATARACT_PATH)}")
    print("Contents:", os.listdir(os.path.dirname(CATARACT_PATH)))

BASE_DST = "dataset"

TRAIN_LIMIT = 200
VAL_LIMIT = 50

# ---------- DIABETIC RETINOPATHY ----------
for folder in ["Mild", "Moderate", "Severe", "Proliferate_DR"]:
    copy_images(
        os.path.join(DR_PATH, folder),
        f"{BASE_DST}/train/diabetic_retinopathy",
        TRAIN_LIMIT // 4
    )

for folder in ["Mild", "Moderate", "Severe", "Proliferate_DR"]:
    copy_images(
        os.path.join(DR_PATH, folder),
        f"{BASE_DST}/val/diabetic_retinopathy",
        VAL_LIMIT // 4
    )

copy_images(
    os.path.join(DR_PATH, "no_dr"),
    f"{BASE_DST}/train/normal",
    TRAIN_LIMIT
)

# ---------- GLAUCOMA ----------
copy_images(
    os.path.join(GLAUCOMA_PATH, "training_set/glaucoma"),
    f"{BASE_DST}/train/glaucoma",
    TRAIN_LIMIT
)

# copy_images(
#     os.path.join(GLAUCOMA_PATH, "training_set/normal"),
#     f"{BASE_DST}/train/normal",
#     TRAIN_LIMIT
# )

copy_images(
    os.path.join(GLAUCOMA_PATH, "test_set/glaucoma"),
    f"{BASE_DST}/val/glaucoma",
    VAL_LIMIT
)

copy_images(
    os.path.join(GLAUCOMA_PATH, "test_set/normal"),
    f"{BASE_DST}/val/normal",
    VAL_LIMIT
)

# ---------- CATARACT ----------
copy_images(
    os.path.join(CATARACT_PATH, "train/cataract"),
    f"{BASE_DST}/train/cataract",
    TRAIN_LIMIT
)

# copy_images(
#     os.path.join(CATARACT_PATH, "train/normal"),
#     f"{BASE_DST}/train/normal",
#     TRAIN_LIMIT
# )

copy_images(
    os.path.join(CATARACT_PATH, "test/cataract"),
    f"{BASE_DST}/val/cataract",
    VAL_LIMIT
)

copy_images(
    os.path.join(CATARACT_PATH, "test/normal"),
    f"{BASE_DST}/val/normal",
    VAL_LIMIT
)

print("✅ Dataset prepared successfully")
