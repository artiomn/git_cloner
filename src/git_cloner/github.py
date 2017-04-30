import git
import os
import json
from pprint import pprint

from .common import connect_with_auth


class GithubCloner(object):
    def __init__(self, site, owner, login='', password=''):
        self.login = login
        self.password = password
        self.site = site
        self.owner = owner

    def _clone_github_repo(self, repo):
        repo_name = repo['name']
        result_path = repo_name

        try:
            clone_url = repo['clone_url']
        except KeyError:
            print('"{}" was not cloned!'.format(result_path))
            return

        if os.path.isdir(result_path):
            try:
                print('Pull "{}"...'.format(result_path))
                git.Git(result_path).pull()
            except Exception as e:
                print('Pull "{}" error: {}'.format(result_path, str(e)))
        else:
            print('Cloning "{}"...'.format(result_path))
            git.Git().clone(clone_url, result_path)

    def _clone_github_projects(self):
        repos = connect_with_auth('api.{}'.format(self.site), path='/users/{}/repos'.format(self.owner)).\
            decode('utf-8')

        repos = json.loads(repos)

        with open('repos.json', 'w') as f:
            pprint(repos, stream=f)

        for repo in repos:
            self._clone_github_repo(repo)

    def clone(self):
        return self._clone_github_projects()
