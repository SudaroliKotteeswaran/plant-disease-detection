#!/usr/bin/env python3
import argparse, json, numpy as np, os, time, logging, random
from keras.models import load_model
from utils import load_image_as_array, load_json
from tts_engine import speak, set_language
from colors import bcolors, colorize, wave_title, sparkle_effect, spinner, progress_bar
from tkinter import Tk, filedialog
import sys

# Base folder for executable or script
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Ensure logs folder exists relative to exe
LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(LOGS_DIR, 'infer.log'),
                    format='%(asctime)s %(levelname)s: %(message)s')

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.h5')
CLASS_MAP_PATH = os.path.join(BASE_DIR, 'models', 'class_indices.json')
LABELS_META = os.path.join(BASE_DIR, 'resources', 'labels.json')
TIPS = os.path.join(BASE_DIR, 'resources', 'farmer_tips.json')
SAMPLE_DIR = os.path.join(BASE_DIR, 'resources', 'samples')
DEFAULT_SAMPLE = os.path.join(BASE_DIR, 'resources', 'sample_tomato.jpg')

SEVERITY_THRESHOLDS = {"low": 0.6, "medium": 0.8, "high": 0.95}

LANG_OPTIONS = {
    "1": ("English", "en"),
    "2": ("தமிழ் (Tamil)", "ta"),
    "3": ("हिंदी (Hindi)", "hi"),
    "4": ("मराठी (Marathi)", "mr")
}

# ---------- Browse file dialog ----------
def browse_file():
    Tk().withdraw()
    filename = filedialog.askopenfilename(
        title="Select Crop Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    return filename

# ---------- Existing functions ----------
def load_model_and_map():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train or place a model at models/best_model.h5")
    model = load_model(MODEL_PATH)
    with open(CLASS_MAP_PATH, 'r') as f:
        class_indices = json.load(f)
    return model, {v: k for k, v in class_indices.items()}

def severity_from_confidence(conf):
    if conf < SEVERITY_THRESHOLDS['low']:
        return "Low", bcolors.OKGREEN
    if conf < SEVERITY_THRESHOLDS['medium']:
        return "Medium", bcolors.OKCYAN
    if conf < SEVERITY_THRESHOLDS['high']:
        return "High", bcolors.ORANGE
    return "Very High", bcolors.FAIL

def get_random_tip(tips_data, lang='en'):
    if not tips_data: return "Follow good agricultural practices."
    tip_obj = random.choice(tips_data)
    return tip_obj.get(f"tip_{lang}", tip_obj.get('tip_en', ''))

def recommend_actions(label_meta, severity):
    organic = label_meta.get('organic', [])
    chemical = label_meta.get('chemical', [])
    prevention = label_meta.get('prevention', [])
    recs = {}
    recs['organic'] = organic
    recs['chemical'] = chemical if severity in ["High", "Very High"] else ["Use only if needed; prefer organic"]
    recs['prevention'] = prevention
    return recs

# ---------- Get metadata with default ----------
def get_label_metadata(label_meta_all, top_label):
    default_meta = {
        "crop": "Unknown",
        "disease": top_label,
        "description": "This disease metadata is not available. Follow general good farming practices.",
        "causative_agent": "Unknown pathogen",
        "botanical_name": "Not available",
        "sample_image": DEFAULT_SAMPLE,
        "organic": [
            "Maintain proper watering and soil nutrition",
            "Use compost or organic manure"
        ],
        "chemical": [
            "Use chemical treatment only if necessary; prefer organic alternatives"
        ],
        "prevention": [
            "Monitor crops regularly",
            "Practice crop rotation",
            "Sanitize tools and equipment"
        ]
    }
    return label_meta_all.get(top_label, default_meta)

def box_header(text, color=bcolors.HEADER):
    line = "═" * (len(text) + 4)
    print(color + f"╔{line}╗" + bcolors.ENDC)
    print(color + f"║  {text}  ║" + bcolors.ENDC)
    print(color + f"╚{line}╝" + bcolors.ENDC)

# ---------- Start screen ----------
def start_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    wave_title("🌱 AI CROP DOCTOR 🌱", cycles=1, beep=True)
    sparkle_effect("Making Farming Smarter ✨")
    print(colorize("\n[1] Upload / Enter Image Path", bcolors.OKBLUE))
    print(colorize("[2] Demo Mode (Sample Images)", bcolors.WARNING))
    print(colorize("[3] Quit\n", bcolors.FAIL))
    choice = input("👉 Enter choice: ").strip()
    return choice

def choose_language():
    print("\nSelect Language:")
    for key, (name, _) in LANG_OPTIONS.items():
        print(f"[{key}] {name}")
    lang_choice = input("👉 Enter choice: ").strip()
    if lang_choice in LANG_OPTIONS:
        return LANG_OPTIONS[lang_choice][1]
    return "en"

# ---------- CLI inference ----------
def cli_infer(image_path, lang):
    if not image_path or not os.path.exists(image_path):
        print(colorize("⚠️ Invalid or missing image path! Using sample image instead.", bcolors.WARNING))
        image_path = DEFAULT_SAMPLE

    spinner("Loading model", 2)
    model, idx_to_label = load_model_and_map()
    label_meta_all = load_json(LABELS_META)
    tips = load_json(TIPS)
    set_language(lang)

    img_arr = load_image_as_array(image_path, target_size=(224, 224))
    x = np.expand_dims(img_arr, axis=0)
    progress_bar(20, "Running Inference")

    start = time.time()
    preds = model.predict(x)[0]
    inf_time = time.time() - start
    top_idx = int(np.argmax(preds))
    top_label = idx_to_label[top_idx]
    top_conf = float(preds[top_idx])

    severity, sev_color = severity_from_confidence(top_conf)
    label_meta = get_label_metadata(label_meta_all, top_label)
    recs = recommend_actions(label_meta, severity)

    # Enhanced Report
    print("🌱 Smart Agriculture - Crop Health Report 🌱\n")
    box_header("CROP HEALTH REPORT", bcolors.OKBLUE)
    print(f"{bcolors.BOLD}Image Path       :{bcolors.ENDC} {image_path}")
    print(f"{bcolors.BOLD}Inference Time   :{bcolors.ENDC} {inf_time:.2f}s")
    print(f"{bcolors.BOLD}Crop             :{bcolors.ENDC} {label_meta.get('crop','-')}")
    print(f"{bcolors.BOLD}Diagnosis        :{bcolors.ENDC} {label_meta.get('disease','-')}")
    print(f"{bcolors.BOLD}Causative Agent  :{bcolors.ENDC} {label_meta.get('causative_agent','-')}")
    print(f"{bcolors.BOLD}Botanical Name   :{bcolors.ENDC} {label_meta.get('botanical_name','-')}")
    print(f"{bcolors.BOLD}Confidence       :{bcolors.ENDC} {top_conf*100:.2f}%")
    print(f"{bcolors.BOLD}Severity         :{bcolors.ENDC} {colorize(severity, sev_color)}")
    print(f"{bcolors.BOLD}Description      :{bcolors.ENDC} {label_meta.get('description','-')}\n")

    box_header("RECOMMENDATIONS", bcolors.ORANGE)
    print(colorize("🌿 Organic Options:", bcolors.OKGREEN + bcolors.BOLD))
    for o in recs['organic']: print(" -", o)
    print(colorize("\n🧪 Chemical Options:", bcolors.WARNING + bcolors.BOLD))
    for c in recs['chemical']: print(" -", c)
    print(colorize("\n🛡 Prevention:", bcolors.OKBLUE + bcolors.BOLD))
    for p in recs['prevention']: print(" -", p)

    box_header("FARMER TIP OF THE DAY", bcolors.HEADER)
    print("💡", get_random_tip(tips, lang))

    speak_text = f"Diagnosis: {label_meta.get('disease','unknown')}. Confidence {top_conf*100:.1f} percent. Severity {severity}."
    speak(speak_text)

# ---------- MAIN ----------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Crop Doctor")
    parser.add_argument('--image', help='Path to plant image')
    parser.add_argument('--lang', choices=['en','hi','ta','mr'], help='Language for TTS')
    args = parser.parse_args()

    if not args.image:
        choice = start_screen()
        if choice == "1":
            lang = choose_language()
            print("\n[1] Browse File\n[2] Enter Path Manually")
            sub_choice = input("👉 Enter choice: ").strip()
            if sub_choice == "1":
                img = browse_file()
            else:
                img = input("📸 Enter path of crop image: ")
            cli_infer(img, lang)

        elif choice == "2":
            lang = choose_language()
            samples = [
                "Tomato__Bacterial_spot",
                "Tomato__Early_blight",
                "Tomato__healthy",
                "Tomato__Late_blight",
                "Tomato__Leaf_Mold",
                "Tomato__Septoria_leaf_spot",
                "Tomato___Spider_mites Two-spotted_spider_mite",
                "Tomato__Target_spot",
                "Tomato__Tomato_mosaic_virus",
                "Tomato__Tomato_Yellow_Leaf_curl_virus"
            ]
            print("\nSelect a sample for Demo Mode:")
            for i, name in enumerate(samples, 1):
                print(f"[{i}] {name.replace('__', ' - ')}")
            sample_choice = input("👉 Enter choice: ").strip()
            if sample_choice.isdigit() and 1 <= int(sample_choice) <= len(samples):
                img = os.path.join(SAMPLE_DIR, samples[int(sample_choice)-1], "sample.jpg")
            else:
                img = DEFAULT_SAMPLE
            cli_infer(img, lang)

        else:
            print(colorize("Exiting... 👋", bcolors.OKCYAN))
    else:
        cli_infer(args.image, args.lang or "en")
