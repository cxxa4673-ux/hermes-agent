---
title: Hermes Agent
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: Hermes Agent Space - runtime check and prompt cost playground
---

# Hermes Agent

This Space is deployed automatically from
[github.com/cxxa4673-ux/hermes-agent](https://github.com/cxxa4673-ux/hermes-agent)
by the `Deploy to Hugging Face Space` GitHub Actions workflow
(`.github/workflows/sync-to-hf.yml`).

**Everything in this Space comes from the `hf-space/` folder of that repo.**
Edit the files there, push to `main`, and this Space rebuilds on its own —
do not edit files here directly, they will be overwritten on the next deploy.

## What it does

- **Ping** — round-trips a string through the Space runtime to prove the app is live.
- **Prompt cost playground** — character/word/token counts and a rough cost estimate.

Runs on CPU with no external API calls, so it boots quickly and free.

## Local preview

```bash
cd hf-space
pip install gradio
python app.py
```
