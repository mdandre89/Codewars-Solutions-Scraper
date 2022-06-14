# Codewars Scraper

This program allows you to connect to [Codewars](https://www.codewars.com) by using your credentials
(through the GitHub OAuth sign in option) and extract all the code of each programming language of
every kata you have completed.

**It's discouraged to put your Codewars solutions publicly available because, even though it depends
on every person and it's a responsibility of one self, having your solutions publicly available may
increase the number of dishonest users that copy and paste the solutions to their own advantage. An user
can get sanctioned if the Codewars' staff notice an unusual behaviour. Read the
[Codewars Code of Conduct](https://docs.codewars.com/community/rules/) for more information (especially
the last rule).**

**Although it's not prohibited, please: don't put your Codewars solutions publicly available on GitHub.
Keep your repository private.**

## Usage

### Requirements

To use this program you need:

- Python3.7+
- A Codewars account.
- A GitHub account.
- Google Chrome 102.0.5005.115+(or compatible with chromedriver 102.0.5005.61)

### All-in-one method

To use this program you just need an initial configuration. After that, you just have to sit down and watch
everything being pulled automatically. Below is the ordered list of steps you must follow to get all working:

1. Click on the green button "Use this template".
2. Choose a name for your repository, mark the "Private" option and click on "Create repository from template".
3. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or [add remotely](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) to pull the new repository locally in your machine.
4. Move to the `
Codewars-Solutions-Scraper` folder.
5. Run the program by writing `python3 main.py YOUR_CODEWARS_USERNAME YOUR_GITHUB_USERNAME YOUR_GITHUB_PASSWORD` in your command line.
6. Wait for the program to complete (you'll see a message that indicates the completion status).
7. Add all the files to the stage, commit them and push them to your private repository.


### Docker

The Docker implementation is still a work in progress.

 - To build: `docker build --no-cache -t Codewars-Solutions-Scraper .`

 - To run: `docker run -it Codewars-Solutions-Scraper YOUR_CODEWARS_USERNAME YOUR_GITHUB_USERNAME YOUR_GITHUB_PASSWORD`

 - To debug: `docker run -it --entrypoint sh Codewars-Solutions-Scraper`


## Disclaimer

This repository is under the [BSD-2-Clause License](LICENSE) to follow
[Codewars's Terms of Service](https://www.codewars.com/about/terms-of-service) (that were last updated
on October, 2018).

If you've read above sections, you know you can customise the program to make it work as you want. Keep in
mind that **I offer the program as you see in this repository**. Any changes you made in your private repository
are up to you, and I'm not responsible for them. Be careful on what you change. For more related information,
please read the ["Privacy" page](https://github.com/JoseDeFreitas/CodewarsGitHubLogger/wiki/Privacy) of the
wiki. I encourage you to read the whole wiki, too.