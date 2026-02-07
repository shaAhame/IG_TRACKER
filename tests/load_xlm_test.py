import sys
from transformers import pipeline

labels = [
    "iPhone",
    "iPad",
    "MacBook",
    "Samsung Galaxy",
    "Redmi",
    "Apple Watch",
    "Google Pixel",
    "OnePlus",
    "Sony",
]

text = "Selling iPhone 15 Pro Max 256GB, excellent condition"

try:
    print("[TEST] Initializing pipeline (this will download the model if needed)...")
    clf = pipeline(
        "zero-shot-classification", model="joeddav/xlm-roberta-large-xnli", device=-1
    )
    print("[TEST] Model loaded. Running prediction...")
    out = clf(text, labels, multi_class=False)
    print("[TEST] Prediction result:\n", out)
    sys.exit(0)
except Exception as e:
    print(f"[TEST] Error: {e}")
    sys.exit(2)
