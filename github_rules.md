# GitHub Rules

## Branches

| Branch | Purpose |
|---|---|
| `main` | Production. Stable releases only. |
| `develop` | Integration of QA-approved features. |
| `qa` | Quality assurance (QA) and testing of features. |
| `feature/fsdc-XXXX` | One ticket per branch, e.g. `feature/fsdc-0001`. |

## Flow

```text
feature/fsdc-XXXX -> qa -> develop -> main (prod)
```

1. Branch features from the latest `develop` (from `main` until `develop` exists).
2. Name: `feature/fsdc-` + 4-digit ticket number.
3. Push the feature branch and open a pull request (PR) into `qa`.
4. After QA passes, open a PR from `qa` into `develop`.
5. For release, open a PR from `develop` into `main`.

## Permissions

- No merge happens without explicit owner approval.
- `qa -> develop` and `develop -> main` always require explicit owner approval.
- Never push directly to `main`, `develop`, or `qa`. Changes enter only through PRs.
- Never force-push or rewrite history on `main`, `develop`, or `qa`.

## Pull requests

- Title: `[FSDC-XXXX] Short description`.
- Body: summary, changed files, test results, linked items from `redevelopment.md`.
- Tests and the app must run before requesting review.
- One ticket per PR. Keep PRs small.

## Commits

- Clear, imperative messages, e.g. `Fix HUD drawn once per particle`.
- Reference the ticket: `FSDC-0001: ...`.
