# grtnr.com_src

This is the source of the Website [grtnr.com](https://grtnr.com) and it's test site [test.grtnr.com](https://test.grtnr.com).

- [grtnr.com\_src](#grtnrcom_src)
  - [Get things up \& running](#get-things-up--running)
  - [Creating \& publishing content](#creating--publishing-content)
  - [Problems / Solutions](#problems--solutions)
    - [Git topics](#git-topics)

## Get things up & running

In order to get things running

- Make sure you have Python installed. I work with Python 3.12
- Create a local python environment: `python -m venv .venv` anc activate it: `source .venv/bin/activate`
- Upgrade your pip: `pip install --upgrade pip`
- Install the required packages: `pip install -r .devcontainer/requirements.txt`
- Build it: `pelican`
- In the dev process, you probably want to run it, keep it watching file changes and serve the website: `pelican -r -l`

To work in a Github Codespace, start a Codespace and build it with `pelican`.

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

