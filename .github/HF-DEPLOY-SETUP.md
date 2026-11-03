# Deploy to Hugging Face — one-time install

The deploy workflow was blocked from being committed by the automation token
(it lacks the GitHub App `workflows` permission), so it lives here as
`hf-deploy.workflow.yml`. Move it into place once, from your own clone:

```bash
git pull
mkdir -p .github/workflows
git mv .github/hf-deploy.workflow.yml .github/workflows/sync-to-hf.yml
git commit -m "ci: enable Hugging Face deploy workflow"
git push
```

(Or in the browser: open this file, copy the content, then
*Add file → Create new file*, name it `.github/workflows/sync-to-hf.yml`, paste, commit.)

After that, every push to `main` that touches `hf-space/**` pushes
`hf-space/` to <https://huggingface.co/spaces/cxxa4673/hermes-agent>.

## Required setup

1. **Space exists** with **SDK: Gradio** — <https://huggingface.co/new-space>
2. **Secret `HF_TOKEN`** in the GitHub repo (not the Space):
   Settings → Secrets and variables → Actions → New repository secret.
   The token must be a **Write** token — <https://huggingface.co/settings/tokens>

```bash
gh secret set HF_TOKEN --repo cxxa4673-ux/hermes-agent
```

3. Actions must be enabled: Settings → Actions → General → *Allow all actions*.

## Why the upstream CI never starts

The inherited workflows request `runs-on: blacksmith-4vcpu-ubuntu-2404`
(and other `blacksmith-*` labels). Blacksmith is a third-party runner
provider that the upstream project has installed; this account does not,
so those jobs stay in "Waiting for a runner to pick up this job" forever.

Fix: either install the Blacksmith GitHub App, or stop running the inherited
CI on this fork — Settings → Actions → General, or per workflow:

```bash
gh workflow disable "CI"
gh workflow disable "Docker Build, Test, and Publish"
gh workflow disable "Nix flake check"
gh workflow disable "auto-fix lint issues & formatting"
```

The HF deploy workflow intentionally uses `runs-on: ubuntu-latest`, so it is
never affected by this.
