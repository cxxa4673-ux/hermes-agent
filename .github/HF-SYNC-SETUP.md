# Hugging Face sync

The active workflow is `.github/workflows/sync-to-hugging-face.yml`. It mirrors
this repository's files to the private Space `cxxa4673/hermes-agent`.

## How the mirror works

- Pushes to GitHub `main` trigger a sync. Manual uploads are also main-only.
- The workflow clones the Space's current `main`, replaces its files with the
  GitHub snapshot, and commits on top of the Space's existing history.
- Space-only files are removed. The repository owner explicitly approved this
  mirror behavior.
- The push is **not forced**. If someone updates the Space after the workflow
  clones it, the push fails instead of overwriting that concurrent work.
- GitHub is checked out with depth 1. The Space receives the current files, not
  GitHub's unrelated commit history.
- `HF_TOKEN` must remain a GitHub Actions repository secret with write access to
  the Space. Never put its value in a source file, remote URL, or chat.
- The workflow uses `ubuntu-latest` and its own concurrency group, so inherited
  Blacksmith CI queues do not block it.

## Check status without uploading

From **Actions → Sync to Hugging Face → Run workflow**, enable
**Only report the private Space status; do not upload files**. This read-only
check can also run from a feature branch and reports the Space SDK, runtime
stage, and hardware in the job summary.

Or use the GitHub CLI:

```sh
gh workflow run sync-to-hugging-face.yml --ref main -f check_only=true
```

## If the GitHub integration cannot update workflow files

The connected integration may lack the GitHub App `workflows` permission. In
that case the same validated workflow is staged at `.github/hf-sync.workflow.yml`.
The repository owner can copy its contents into
`.github/workflows/sync-to-hugging-face.yml` through the GitHub web editor and
commit to `main`, or apply the change from their own local Git checkout.

## Sync success is not app health

A green sync confirms the upload and reports the Space status at that moment.
Check the private Space's build and container logs before calling the deployment
healthy. The current root README has no Hugging Face SDK metadata, and the root
Dockerfile has an empty default CMD. A Docker Space needs valid SDK metadata, a
startup command, the correct listening port (normally 7860), and any required
runtime secrets. A Gradio Space needs a Gradio entrypoint; mirroring this whole
repository alone does not provide one.

The dashboard must not be exposed without its authentication provider. Configure
the supported dashboard auth secrets in the Space rather than disabling auth.
