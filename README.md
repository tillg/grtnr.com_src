# grtnr.com_src

This is the source of the Website [grtnr.com](https://grtnr.com) and it's test site [test.grtnr.com](https://test.grtnr.com).

[TOC]

## Get things up & running

In order to get things running

- Make sure you have Python installed. I work with Python 3.12
- Create a local python environment: `python -m venv .venv` anc activate it: `source .venv/bin/activate`
- Upgrade your pip: `pip install --upgrade pip`
- Install the required packages: `pip install -r .devcontainer/requirements.txt`
- Build it: `inv build`
- In the dev process, you probably want to run it with live reloading: `inv livereload`

To work in a Github Codespace, start a Codespace and build it with `inv build`.

### Available invoke tasks

This project uses invoke for task automation. Here are the available commands:

- `inv build` - Build local version of site
- `inv rebuild` - Build with the delete switch (clean rebuild)
- `inv clean` - Remove generated files
- `inv serve` - Serve site at <http://localhost:8000/>
- `inv reserve` - Build then serve the site
- `inv regenerate` - Automatically regenerate site upon file modification
- `inv livereload` - Build with live reloading (recommended for development)
- `inv preview` - Build production version of site

## Code Quality

This project uses automated Python code formatting and linting. For detailed guidelines, tool configurations, and development workflows, see [CODE_GUIDELINES.md](CODE_GUIDELINES.md).

**Quick commands:**

- `inv format-py` - Format Python code
- `inv lint-py` - Run linting
- `inv check-py` - Format and lint (recommended before commits)

## Creating & publishing content

The general process to publish is automated by Github actions:

- Committing to branch `main` publishes to `grtnr.com`,
- Committing to another branch publishes to `test.grtnr.com`.

The branching & committing process:

```bash
# Create a new branch
git branch my-new-feature
git checkout my-new-feature

# Make your changes and commit them to the branch
git add --all
git commit -m "Add feature X"

# Push your branch to the remote repository:
git push origin my-new-feature
# This will trigger the deployment to test.grtnr.com
```

Once you checked everything on `test.grtnr.com` this is how you deploy to `grtnr.com` (via creating a Pull Request):

- Go to your repository on GitHub
- Click on "Pull requests" and then "New pull request"
- Set the base branch to "main" and the compare branch to "my-new-feature"
- Click "Create pull request"
- Give your PR a title and description explaining your changes
- Click "Create pull request" again
- On the PR page, once you're ready to merge, click "Merge pull request" and then "Confirm merge"

Once this is done u need to update your loacl environment:

```bash
# Switch back to the main branch
git checkout main

# Pull the latest changes from the remote main branch
git pull origin main
# This will bring in the changes you merged via PR

# Clean up by deleting your local copy of the now-deleted remote branch
git branch -d my-new-feature
```

## Problems / Solutions

### Git topics

I have started to change the code in my editor (including saving many files) w/o having created & checked out a new branch. How do i now make it into a branch?

This is how u do it:

```bash
# First, check what files you've modified
git status

# Create a new branch and switch to it, bringing all your changes with you
git checkout -b your-new-branch-name

# Now add all the modified files to staging
git add --all

# Commit your changes to the new branch
git commit -m "Your descriptive commit message"

# Push the new branch to GitHub to trigger deployment to test.grtnr.com
git push origin your-new-branch-name
```
