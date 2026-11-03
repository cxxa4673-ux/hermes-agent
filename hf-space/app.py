"""Hermes Agent — Hugging Face Space entrypoint.

This is the minimal, dependency-light app the Space boots. It runs fully on
CPU (no model download, no API key), so the Space goes green in seconds and
you can verify the deploy pipeline end to end.

Replace/extend it with a real model call later; the deploy workflow
(.github/workflows/sync-to-hf.yml) simply mirrors this hf-space/ folder to
https://huggingface.co/spaces/cxxa4673/hermes-agent on every push to main.
"""

from __future__ import annotations

import platform
import sys

import gradio as gr

APP_TITLE = "Hermes Agent"

PRICE_PER_MTOK_INPUT = 0.15
PRICE_PER_MTOK_OUTPUT = 0.60


def runtime_info() -> str:
    return (
        f"- **App**: {APP_TITLE}\n"
        f"- **Python**: {sys.version.split()[0]}\n"
        f"- **Platform**: {platform.platform()}\n"
        f"- **Status**: running on the Hugging Face Space ✅"
    )


def ping(name: str) -> str:
    who = (name or "").strip() or "world"
    return f"Hello {who} — the Space is alive and this function ran on the server."


def analyse(text: str) -> tuple[str, str]:
    """Cheap, offline prompt statistics + rough token/cost estimate."""
    text = text or ""
    chars = len(text)
    words = len(text.split())
    lines = text.count("\n") + (1 if text.strip() else 0)
    # ~4 characters per token is the usual English rule of thumb.
    tokens = max(1, round(chars / 4)) if chars else 0

    stats = (
        f"| metric | value |\n|---|---|\n"
        f"| characters | {chars} |\n"
        f"| words | {words} |\n"
        f"| lines | {lines} |\n"
        f"| est. tokens | {tokens} |"
    )
    cost_in = tokens / 1_000_000 * PRICE_PER_MTOK_INPUT
    resp_tokens = tokens * 2  # naive "reply is ~2x the prompt" guess
    cost_out = resp_tokens / 1_000_000 * PRICE_PER_MTOK_OUTPUT
    cost = (
        f"Rough estimate at ${PRICE_PER_MTOK_INPUT}/M input tokens and "
        f"${PRICE_PER_MTOK_OUTPUT}/M output tokens:\n\n"
        f"- input: **{tokens}** tokens → **${cost_in:.6f}**\n"
        f"- a ~{resp_tokens}-token reply → **${cost_out:.6f}**\n"
        f"- total per request ≈ **${cost_in + cost_out:.6f}**"
    )
    return stats, cost


with gr.Blocks(title=APP_TITLE) as demo:
    gr.Markdown(f"# {APP_TITLE}\nDeployed from GitHub Actions to a Hugging Face Gradio Space.")
    gr.Markdown(runtime_info())

    with gr.Tab("Ping"):
        with gr.Row():
            name_in = gr.Textbox(label="Your name", placeholder="type anything")
            ping_out = gr.Textbox(label="Server response", interactive=False)
        ping_btn = gr.Button("Send", variant="primary")
        ping_btn.click(ping, inputs=name_in, outputs=ping_out)
        name_in.submit(ping, inputs=name_in, outputs=ping_out)

    with gr.Tab("Prompt cost playground"):
        gr.Markdown("Paste a prompt and get character/word counts plus a rough token & cost estimate. Runs entirely on CPU.")
        prompt_in = gr.Textbox(label="Prompt", lines=8, placeholder="Paste your prompt here…")
        with gr.Row():
            stats_out = gr.Markdown()
            cost_out = gr.Markdown()
        analyse_btn = gr.Button("Analyse", variant="primary")
        analyse_btn.click(analyse, inputs=prompt_in, outputs=[stats_out, cost_out])
        prompt_in.change(analyse, inputs=prompt_in, outputs=[stats_out, cost_out], show_progress=False)

if __name__ == "__main__":
    demo.launch()
