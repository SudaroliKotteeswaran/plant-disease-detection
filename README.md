1. I open Command Prompt and go to Desktop:

```
cd %USERPROFILE%\Desktop
```

2. I clone only the `cropcli` branch:

```
git clone -b cropcli --single-branch https://github.com/SudaroliKotteeswaran/plant-disease-detection.git
cd plant-disease-detection
```

3. I install Git LFS (if models are large) and pull LFS files:

```
git lfs install
git lfs pull
```

4. I create and activate a Python virtual environment (Windows):

```
python -m venv venv
venv\Scripts\activate
```

(If on mac/linux: `python3 -m venv venv` then `source venv/bin/activate`)

5. I upgrade pip and install requirements:

```
pip install --upgrade pip
pip install -r requirements.txt
```

6. I check that model files exist in the `models/` folder:

```
dir models   # Windows
# or
ls -la models
```

If missing, I download the model(s) and put them into `models/` (use Drive/Hugging Face link).

7. I read the inference help to know arguments:

```
python infer.py --help
```

8. I run inference
   //python infer.py
