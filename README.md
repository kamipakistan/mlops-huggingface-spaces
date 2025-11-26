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

## Live Demo

You can try the app online here: [Text Summarization App](https://huggingface.co/spaces/kamipakistan/text_summarization_app)

# Building an end-to-end MLOps pipeline with Hugging Face Spaces & GitHub Actions
 
This repository demonstrates a simple Continuous Deployment (CD) workflow that automatically syncs your GitHub repo to a Hugging Face Space whenever you push changes. The workflow uses GitHub Actions and a Hugging Face access token to push the app files into your Space's Git repository.

<img width="1920" height="1080" alt="Screenshot from 2025-11-20 16-36-20" src="https://github.com/user-attachments/assets/81d1db19-b535-4eae-acaf-30d44d3e3400" />

## Table of contents

1. Overview
2. Prerequisites
3. Step 1 — Create a Hugging Face Space
4. Step 2 — Configure your GitHub repo
5. Step 3 — Create a Hugging Face access token
6. Step 4 — Add token to GitHub Secrets
7. Step 5 — GitHub Actions workflow (example)
8. Minimal repository layout
9. Tips & troubleshooting
10. Security notes

## Overview
When you push to your GitHub repository, a GitHub Actions workflow will run that:
* checks out your repo,
* optionally installs dependencies/runs tests,
* pushes the application files to your Hugging Face Space repository using the `HF_TOKEN` secret.
This gives you automated deployment of your Gradio/Streamlit app to HF Spaces.

## Prerequisites
* A Hugging Face account.
* A GitHub account and a repository for your ML app.
* Basic knowledge of Git, Python, and YAML.

## Step 1 - Create a Hugging Face Space
1. Go to Hugging Face → Spaces and click Create new Space.
2. Fill in details:
    * Space name: e.g. my-mlops-app
    * License: pick appropriate license
    * Space SDK: Gradio (or Streamlit)
    * Hardware: CPU Basic (free tier) or appropriate hardware
    * Visibility: Public or Private
3. Click Create Space — this provisions a Git repo under `https://huggingface.co/spaces/<HF_USERNAME>/<SPACE_NAME>`.

## Step 2 - Configure your GitHub repository
Make sure your GitHub repo contains the files needed to run the app in the Space:
* `app.py` — your Gradio or Streamlit app entry point.
* `requirements.txt` — Python dependencies required by the Space.
* Optional: `README.md`, model files, `assets/`, `src/`, etc.

## Step 3 - Create a Hugging Face access token
1. In Hugging Face, go to **Profile** → **Settings** → **Access Tokens**.
2. Click **New Token**. Name it and select the write role (so the action can push).
3. Generate and copy the token — you will not be able to see it again after closing.

## Step 4 - Add the access token as a GitHub Secret
1. In your GitHub repository, go to **Settings** → **Security** → **Secrets** and **variables** → **Actions**.
2. Click New repository secret.
    * **Name**: `HF_TOKEN`
    * **Value**: paste the token you copied from Hugging Face
3. Save the secret.

## Step 5 — GitHub Actions workflow (example)
Create the file: `.github/workflows/sync-to-hf-space.yml`
> Replace: `HF_USERNAME` and `SPACE_NAME` with your Hugging Face username and Space name (or use repository/organization name as appropriate). The workflow uses the `HF_TOKEN` secret to authenticate.

**Notes:**
* Replace `HF_USERNAME` and `SPACE_NAME` with your actual Hugging Face username and Space name.
* The workflow clones the remote Space, copies your repo files into it, commits, and pushes. `--force` is used to ensure the remote matches the GitHub repo — remove if you prefer a safer merging strategy.
* You can adjust which branch the workflow pushes to on the Space (here it goes to `main`).

## Minimal repository layout (recommended).
```
├── .github/
│   └── workflows/
│       └── sync-to-hf-space.yml
├── app.py
├── Makefile
├── requirements.txt
├── README.md
└── src/               # optional module code
```
**`requirements.txt:`**

```
gradio         # or streamlit if using Streamlit
transformers
tensorflow
```




