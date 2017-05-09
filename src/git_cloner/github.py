import git
import os
import json
from pprint import pprint

from .common import connect_with_auth


class GithubClonerException(Exception):
    def __init__(self, exc_data):
        self.message = exc_data.get('message', '')

    def __str__(self):
        return self.message


class GithubCloner(object):
    """
    Class to clone Github-style repositories.
    """

    def __init__(self, site, owner, login='', password=''):
        self.login = login
        self.password = password
        self.site = site
        self.owner = owner

    def _download_path(self, path):
        return connect_with_auth('api.{}'.format(self.site),
                                 path=path,
                                 login=self.login,
                                 password=self.password).decode('utf-8')

    def _clone_repo(self, repo):
        repo_name = repo['name']
        result_path = '{}/{}'.format(self.owner, repo_name)

        try:
            clone_url = repo['clone_url']
        except KeyError:
            print('"{}" was not cloned, because has not clone url!'.format(result_path))
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

    def _get_user_list(self, since):
        users = self._download_path('/users?since={}'.format(since))

        if not isinstance(users, list):
            raise GithubClonerException(users)

        return users

    def _clone_user_projects(self):
        repos = self._download_path('/users/{}/repos?per_page=100000'.format(self.owner))

        repos = json.loads(repos)

        if not isinstance(repos, list):
            raise GithubClonerException(repos)

        if not os.path.isdir(self.owner):
            os.mkdir(self.owner)

        print('Repositories count: {}'.format(len(repos)))

        with open('{}/repos.json'.format(self.owner), 'w') as f:
            pprint(repos, stream=f)

        for repo in repos:
            self._clone_repo(repo)

    def _clone_all_projects(self):
        since = 0
        users = self._get_user_list(since)

        while users:
            if not isinstance(users, list):
                raise GithubClonerException(users)

            for user in users:
                self.owner = user.get('login')
                self._clone_user_projects()

            users = self._get_user_list(since)
            since += len(users)

    def clone(self):
        if self.owner:
            return self._clone_user_projects()
        else:
            return self._clone_all_projects()
