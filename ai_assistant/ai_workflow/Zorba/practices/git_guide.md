# Git guide

Use these commands from the repository you are working in. The commit and PR guides explain when to use them and what to record.

## Inspect local changes

```bash
git branch --show-current
git status --untracked-files=all
git diff
git diff --cached
```

Read the unstaged diff and the staged diff separately. Open untracked files directly. To read an untracked text file as a diff, use `git diff --no-index -- /dev/null <file>`. Exit code 1 means the files differ. To narrow a tracked diff to one file or directory, add `-- <path>`.

## Inspect a branch against its base

Check out the branch you want to describe or review. Use the base branch specified for the task. Ask which branch to use if the base is unclear.

```bash
base='<base-branch>'
git rev-parse HEAD
git log --oneline "$base"..HEAD
git diff --stat "$base"...HEAD
git diff "$base"...HEAD
```

Use the commit ID to record the version you inspected. The log lists commits on the active branch that are outside the base. The diff shows the committed changes since the branches diverged. Inspect local changes separately when they are in scope.

## Stage and check changes

Stage the files in the planned commit with `git add -- <path>...`. Use `git add -p -- <path>` to select hunks in a tracked file.

```bash
git diff --cached
git diff --cached --check
```

Read the staged diff to confirm exactly what will be committed. The second command checks for whitespace errors and conflict markers. Verify behavior with the checks appropriate to the project.

## Record and confirm a commit

Put the complete commit message in a plain-text file, then run `git commit -F <message-file>`. Use `git show --format=fuller HEAD` to confirm the recorded hash, message, and changes. Use `git status --untracked-files=all` to see what remains.
