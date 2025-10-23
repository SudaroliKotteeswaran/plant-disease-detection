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

8. I run inference with the correct model and image (example):

```
python infer.py --image resources/samples/sample.jpg --model models/best_model.pth --output output.jpg
```

(Replace `--model` and `--image` with the exact filenames shown by `--help`.)

9. I open `output.jpg` to see the result.

10. If I change code later, I commit and push the branch:

```
git add .
git commit -m "my changes"
git push origin cropcli
```

— end —

If any step shows an error, I copy the full error message and run only the failing command again so I can fix it.
