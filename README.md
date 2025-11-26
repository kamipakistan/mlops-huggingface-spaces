---
title: Text Summarization App
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: cc
---


[![Sync to Hugging Face hub](https://github.com/kamipakistan/mlops-huggingface-spaces/actions/workflows/main.yml/badge.svg)](https://github.com/kamipakistan/mlops-huggingface-spaces/actions/workflows/main.yml)


# End-to-End MLOps: Deploy a Text Summarization App to Hugging Face Spaces (Gradio) with GitHub Actions

**Goal:** build, test locally, and automatically deploy a Gradio-based text summarization app that uses a Hugging Face model and is continuously delivered to a Hugging Face Space via GitHub Actions.

---
### Live Demo
You can try the app online here: [Text Summarization App](https://huggingface.co/spaces/kamipakistan/text_summarization_app)

---


## Quick overview (what you'll end up with)
- A GitHub repository containing a small Gradio app (`app.py`) that uses `transformers` summarization pipeline.
- A `requirements.txt` and `Makefile` to install/run the app locally (CodeSpaces or local machine).
- A GitHub Actions workflow that pushes the repo to a Hugging Face Space when you push to `main`.
- A running HF Space (Gradio) that shows the summarizer UI and updates automatically after each commit.

---

## Prerequisites
- GitHub account.
- Hugging Face account (https://huggingface.co) and ability to create a Space.
- Optional but recommended: GitHub Codespaces (or any dev machine with Python 3.9+).
- `git`, `python3`, `pip` (or use Codespaces which provides those).

---

## 1) Create the Hugging Face Space
1. Sign in to Hugging Face.
2. Go to **Spaces** → **Create new Space**.
   - Name: `text_summarization_app` (or your chosen name). This will create a repo: `https://huggingface.co/spaces/<your-username>/<space-name>`.
   - Select **Gradio** as the SDK.
   - Choose a license if you want.
3. Keep this page open — you will use the Space repo URL later.

---

## 2) Create the GitHub repository
1. Create a new GitHub repo e.g.`mlops-huggingface-spaces` (private or public).
2. Clone it locally or open it in Codespaces.
3. Recommended repo structure (create these files/folders):

```
mlops-huggingface-spaces/
├── .github/
│   └── workflows/
│       └── main.yml
├── app.py
├── requirements.txt
├── Makefile
└── README.md
```

---

## 3) `app.py` (minimal Gradio summarizer)
- This example uses `transformers` pipeline (works with `torch`).

```python
# app.py
from transformers import pipeline
import gradio as gr

summarizer = pipeline('summarization')


def summarize_text(text, max_length=120, min_length=30):
    if not text or len(text.strip()) == 0:
        return "Please supply some text to summarize."
    out = summarizer(text, max_length=int(max_length), min_length=int(min_length))[0]['summary_text']
    return out


with gr.Blocks() as demo:
    gr.Markdown('# Text Summarizer')
    with gr.Row():
        inp = gr.Textbox(label='Input text', lines=8)
        out = gr.Textbox(label='Summary', lines=4)
    maxlen = gr.Slider(30, 512, value=120, step=1, label='Max length')
    minlen = gr.Slider(5, 200, value=30, step=1, label='Min length')
    btn = gr.Button('Summarize')

    btn.click(summarize_text, inputs=[inp, maxlen, minlen], outputs=out)


if __name__ == '__main__':
    demo.launch()
```

> Note: If you prefer TensorFlow models, change the pipeline and dependencies; `transformers` + `torch` is a stable combo.

---

## 4) `requirements.txt`
```
gradio
transformers
torch
```

- If you want smaller models or CPU-only: consider `transformers==4.x` and using model ids that are CPU-friendly (or use `accelerate` / `bitsandbytes` for advanced options). For the tutorial, we'll stick to the default.

---

## 5) `Makefile` (helpful commands)
```
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	python app.py

format:
	black .
```

---

## 6) Local test (Codespaces or local machine)
1. Create and activate a virtual environment: `python -m venv .venv && source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows).
2. `make install` (or `pip install -r requirements.txt`).
3. `make run` or `python app.py`.
4. Open the displayed Gradio link in the browser and test summarization.

---

## 7) Create a Hugging Face access token and store it in GitHub
1. In Hugging Face: profile → Settings → Access Tokens → New token → **read** + **write** (or `write` if shown).
2. Copy the token (one-time view).
3. In GitHub repository: Settings → Secrets and variables → Actions → New repository secret.
   - Name: `HF_TOKEN` (or `HF_API_TOKEN`).
   - Value: paste the HF token.

---

## 8) GitHub Actions workflow to push code to your Space
- The general idea: when you push to `main`, the workflow checks out your repo and pushes to the Hugging Face Space git remote using the token.

Create `.github/workflows/main.yml` with this content:

```yaml
name: Sync to Hugging Face hub

on:
  push:
    branches: [main]

  # to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Add remote 
        env:
          HF: ${{ secrets.HF_TOKEN }}
        run: git remote add space https://kamipakistan:$HF@huggingface.co/spaces/kamipakistan/text_summarization_app

      - name: Push to hub
        env:
          HF: ${{ secrets.HF_TOKEN }}
        run: git push --force https://kamipakistan:$HF@huggingface.co/spaces/kamipakistan/text_summarization_app main
```

**Important:** Replace `<YOUR_HF_USERNAME>` and `<YOUR_SPACE_NAME>` with your `HF` username and space repo name (exactly the same one created earlier). The workflow uses the HF token to authenticate.

---

## 9) Add README and commit
- Add **HF Metadata (your Space config)** to the README.
- Keep it at the top of README.md (this tells Spaces which SDK + version to use):

   ```
   ---
   title: Text Summarization App
   emoji: 📊
   colorFrom: blue
   colorTo: purple
   sdk: gradio
   sdk_version: 5.49.1
   app_file: app.py
   pinned: false
   license: cc
   ---
   ```
- Commit and push to GitHub `main`.

---

## 10) First deployment
1. After pushing to `main`, the GitHub Actions workflow will run.
2. Check Actions tab for the workflow run and logs.
3. If it completes successfully, your HF Space's repository will receive the files and the Space will build and run.
4. Visit your HF Space URL: `https://huggingface.co/spaces/<username>/<space>` and test the UI.

---

## Troubleshooting & tips
- **Large models & timeouts:** Gradio / HF Spaces may timeout or use limited CPU/GPU depending on your Space plan. Use smaller models (e.g., `t5-small` or `sshleifer/distilbart-cnn-12-6`) for faster load and lower memory use.
- **Model selection:** To use a specific model, set `pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')` in `app.py` to ensure CPU-friendly behavior.
- **Secrets:** Keep your HF token secret. If accidentally leaked, revoke it from Hugging Face and create a new one.
- **Git LFS:** If you include large model files or assets, make sure to use `git lfs` properly.

---

## Advanced improvements (next steps)
- Use a smaller CPU-efficient model and pin model name in code.
- Add tests and a GitHub Actions job for unit tests.
- Use a workflow that only deploys when a `deploy` label is added (protect HF Space from accidental deploys).

---

## Appendix — Example files
- `README.md`: short description + usage.
- `app.py`: (already included above).
- `.github/workflows/main.yml`: (included above).

---
