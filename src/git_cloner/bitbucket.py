import git
import os
import json
from pprint import pprint


class BitbucketCloner(object):
    def __init__(self, site, login, password):
        self.login = login
        self.password = password
        self.site = site

    def clone_bitbucket_repo(self, project_key, repo):
        repo_name = repo['name']
        result_path = '{}/{}'.format(project_key, repo_name)

        try:
            clone_links = repo['links']['clone']
        except KeyError:
            print('"{}" was not cloned!'.format(result_path))
            return

        clone_link = ''
        for link in clone_links:
            clone_link = link['href']
            if link['name'] == 'ssh':
                break

        if not clone_link:
            print('"{}" has not clone link!'.format(result_path))
            return

        if os.path.isdir(result_path):
            try:
                print('Pull "{}"...'.format(result_path))
                git.Git(result_path).pull()
            except Exception as e:
                print('Pull "{}" error: {}'.format(result_path, str(e)))
        else:
            print('Cloning "{}"...'.format(result_path))
            git.Git().clone(clone_link, result_path)

    def clone_bitbucket_repos(self, project):
        project_key = project['key']

        try:
            os.mkdir(project_key)
        except FileExistsError:
            pass

        with open('{}/descr.json'.format(project_key), 'w') as f:
            f.write(str(project))

        repos = json.loads(connect_with_auth(path='/rest/api/1.0/projects/{}/repos?limit=10000'.format(project_key)).decode('utf-8'))

        for repo in repos.get('values', []):
            self.clone_bitbucket_repo(project_key, repo)

    def clone_bitbucket_projects(self):
        projects = connect_with_auth(path='/rest/api/1.0/projects?limit=10000').decode('utf-8')

        with open('projects.json', 'w') as f:
            f.write(projects)

        projects = json.loads(projects)

        for project in projects.get('values', []):
            self.clone_bitbucket_repos(project)

