#!/usr/bin/env python3
"""
Script to upload the project to GitHub and trigger compilation via GitHub Actions.
"""

import subprocess
import sys
import os

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    # Check if git is installed
    try:
        run_command("git --version")
    except:
        print("Git is not installed. Please install Git first.")
        sys.exit(1)

    # Check if this is a git repository
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        run_command("git init")
        print("Git repository initialized.")

    # GitHub repository SSH URL
    repo_url = "git@github.com:veeedu/fconverter.git"

    # Check if remote origin exists
    remotes = run_command("git remote")
    if "origin" not in remotes:
        print("Adding remote origin...")
        run_command(f"git remote add origin {repo_url}")
    else:
        print("Remote origin already exists. Updating URL...")
        run_command(f"git remote set-url origin {repo_url}")

    # Add all files
    print("Adding files to git...")
    run_command("git add .")

    # Check if there are changes to commit
    status = run_command("git status --porcelain")
    if not status:
        print("No changes to commit.")
        print("If you want to trigger a build, make sure there are changes or force push.")
    else:
        # Commit
        commit_message = "Upload project for automated build"
        print(f"Committing with message: {commit_message}")
        run_command(f"git commit -m \"{commit_message}\"")

    # Push to GitHub
    print("Pushing to GitHub...")
    try:
        run_command("git push -u origin main")
        print("Successfully pushed to GitHub!")
        print("GitHub Actions will now compile the .exe file.")
        print("Check the Actions tab in your GitHub repository for the build status.")
        print("Once complete, download the OfflineConverter.exe from the workflow artifacts.")
    except:
        print("Push failed. Make sure you have the correct permissions and the repository exists.")
        print("If using HTTPS, you may need to enter credentials or use a personal access token.")
        print("If using SSH, ensure your SSH key is configured.")

if __name__ == "__main__":
    main()