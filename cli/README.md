# fast-cov

CLI for uploading HTML coverage reports to a self-hosted [fast-cov](https://github.com/YuriiMotov/fast-cov) backend, then setting a GitHub commit status with the coverage value.

## Install

```bash
pip install fast-cov
```

Requires Python 3.13+.

## Usage

Upload an HTML coverage report directory:

```bash
fast-cov upload ./htmlcov \
  --api-url https://fast-cov.example.com \
  --api-key "$FAST_COV_API_KEY" \
  --repo-owner my-org \
  --repo-name my-repo \
  --commit-sha "$GITHUB_SHA" \
  --gh-token "$GITHUB_TOKEN" \
  --coverage-threshold 90 \
  --is-default-branch
```

Every option also reads from a matching environment variable (`FAST_COV_API_URL`, `FAST_COV_API_KEY`, `FAST_COV_REPO_OWNER`, `FAST_COV_REPO_NAME`, `FAST_COV_COMMIT_SHA`, `FAST_COV_GH_TOKEN`, `FAST_COV_COVERAGE_THRESHOLD`, `FAST_COV_IS_DEFAULT_BRANCH`), which is the typical way to use it from CI.

`fast-cov upload --help` lists all options.

## What it does

1. Requests a temporary upload session from the fast-cov backend.
2. Uploads every file in the given directory to S3 in parallel (default concurrency: 50).
3. Reads the coverage percentage from `index.html` in the report.
4. Posts a `fast-coverage` commit status to GitHub (`success` if `>= --coverage-threshold`, otherwise `failure`).
5. On the default branch, invalidates the badge cache and purges GitHub's Camo cache for the README badge.

## License

MIT. See the project repository for the full license text.
