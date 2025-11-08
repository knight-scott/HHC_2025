# Write Up Template

## About

This is the template I've modified from [crahan's](https://github.com/crahan) [HolidayHackChallengeTemplate](https://github.com/crahan/HolidayHackChallengeTemplate/). While the original is holiday and CTF competition specific, the general idea and formatting is applicable to any number of reporting scenarios. I hope to utilize this better for creating ongoing reports of CTF challenges I compete in. It's based on [MkDocs](https://www.mkdocs.org) and the [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) theme. 

## Setup

### Set Up Your Python Environment

1. Make a copy of this repository in your own GitHub account. Forking the repository won't work if you wish to change the repository's visibility as a forked repository's visibility can not be changed to _Private_.
2. Clone the copy of the repository to your computer using `git clone <repository_url>`.
3. Navigate into the folder using `cd <cloned_folder_name>`.
4. Create a Python virtual environment using `python3 -m venv venv`.
5. Activate the environment using `. ./venv/bin/activate` (for a Bash shell environment).
6. Install the Python package dependencies using `pip install -r requirements`.
7. Run `mkdocs serve` to start a local copy of the website at `http://127.0.0.1:8000/`.

### Add Your Content

Details such as the site name, site author, and contents of the sidebar navigation are configured in the [`mkdocs.yml`](mkdocs.yml) file. The write-up itself and associated assets are located in the [`docs`](docs/) folder. The default configuration stores the write-up for each objective in a `docs/objectives/oX.md` file and associated images for that objective in a `docs/img/objectives/oX/` folder. As you add content and make changes to files, MkDocs will automatically update the local copy of the website at `http://127.0.0.1:8000/`.

![Files](./img/files.png)

**Note**: More information on how to make changes to MkDocs settings or the Material theme configuration is available at https://www.mkdocs.org/user-guide/writing-your-docs/ and https://squidfunk.github.io/mkdocs-material/reference/, respectively.

### Publish Your Report

**IMPORTANT**: If competing in a CTF competition, it may be a good idea to set your repository visibility to _Private_ until the approved publication dates. This way, no solutions or spoilers are accidentally leaked to the public!

When ready to share your finalized report with the world, there are a couple of options. Run the `mkdocs gh-deploy` command in a terminal to create all the required HTML assets and push them to a `gh-pages` branch on GitHub. To serve the HTML content as a website go the _Pages_ section in the GitHub settings for the repository, select _Deploy from a branch_ for the _Source_ and make sure the _Branch_ is set to _gh-pages_.  

![GitHub Settings](./img/github_settings.png)

After a few minutes your write-up will be live at `https://<username>.github.io/<repository>`, with `<username` your GitHub username and `<repository>` the name of your GitHub repository. This will require setting the visibility to _Public_ though unless you have a paid membership. If you are working on something in stages, and would like to publish only the completed portions, without making both your draft and published repository _Public_, you can consider setting up a mirror repository.

## Mirror Repository

If for some reason you do not want to make the write up repository publicly visible, you can create a **Published** branch and mirror repository. To do so, create a new _Public_ repository in GitHub. Then push the published/completed content to the public repository:

```bash linenums="1" title="Mirror Setup"
# Add the new public repository as a remote
git remote add public git@github.com:<your-username>/<public-repository-name>.git

# Push the gh-pages branch to the public repository
git push public gh-pages
```
You can then continue the instructions above to serve the HTML content as a website.