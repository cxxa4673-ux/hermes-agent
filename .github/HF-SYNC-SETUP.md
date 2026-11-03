# Enable the Hugging Face sync

The connected GitHub integration cannot write files under `.github/workflows/`.
The validated workflow is therefore staged at `.github/hf-sync.workflow.yml`.
GitHub does **not** run it from that location. The repository owner must install
it once using their own GitHub account.

## Install after merging the workflow-fix PR

1. Open [the workflow template](hf-sync.workflow.yml) and copy its contents.
2. In the GitHub repository, select the `main` branch, then **Add file → Create
   new file**.
3. Name the file `.github/workflows/sync-to-hugging-face.yml` and paste the contents.
4. Commit the new file to `main`.

Alternatively, from a local checkout with the merged fix:

```sh
git switch main
git pull --ff-only origin main
mkdir -p .github/workflows
git mv .github/hf-sync.workflow.yml .github/workflows/sync-to-hugging-face.yml
git commit -m "ci: enable Hugging Face sync"
git push origin main
```

The commit to `main` triggers **Sync to Hugging Face**. It can also be started
from **Actions → Sync to Hugging Face → Run workflow → main** after installation.
The job deliberately skips manual runs from other branches.

## Credentials and target

- The owner has confirmed that the GitHub Actions repository secret `HF_TOKEN`
  exists. Never put its value in a source file, command-line URL, or chat.
- The token needs write access to the private Space
  `cxxa4673/hermes-agent`.
- The workflow uses GitHub-hosted `ubuntu-latest` and its own concurrency group;
  it does not wait for the inherited Blacksmith CI jobs.
- The push is non-force. If the Space has unrelated Git history, the job fails
  instead of silently overwriting it. Reconcile the histories deliberately before
  retrying; do not solve this by putting a token in a remote URL.

## Verify the result

A green Actions job confirms the Git push, not that the application is healthy.
Check the private Space's build and container logs separately. The repository's
current root README has no Hugging Face SDK metadata, and its Dockerfile has an
empty default CMD. A Docker Space therefore also needs a valid startup command,
the correct listening port (normally 7860), and any required runtime secrets.
If the existing Space uses Gradio instead, this whole-repository mirror is not a
Gradio app payload; decide which application should be deployed before changing
the Space's files or SDK.
