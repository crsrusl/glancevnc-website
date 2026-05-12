# Agent Instructions

These instructions apply to the whole repository.

## Finish Workflow

When work is complete:

1. Run the relevant tests or validation checks for the change.
   - Prefer the repository's documented test, build, lint, or validation commands.
   - If no automated checks exist, perform the best available manual validation and state that no automated test command was found.
   - Do not skip testing silently.
2. Review `git status` and stage only the files that belong to the completed work.
3. Commit the completed work on `main` with a clear commit message.
4. Push `main` to the configured remote.
5. Report the validation performed, commit hash, and push result.

Do not include unrelated user changes in the commit unless the user explicitly asks for them.
