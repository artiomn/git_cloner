#!/usr/bin/python3


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', type=str, nargs=1, help='service type: `bitbucket` or `github`')
    parser.add_argument('--login', '-l', type=str, nargs=1, default=[''], help='user login')
    parser.add_argument('--password', '-p', type=str, nargs=1, default=[''], help='user password')
    parser.add_argument('--owner', '-o', type=str, nargs=1, default=[''], help='repositories set owner')

    parser.add_argument('site', metavar='site', type=str, help='service address')

    args = parser.parse_args()

    service_type = None if args.type is None else args.type[0]
    site = args.site
    login = args.login[0]
    password = args.password[0]
    owner = args.owner[0]

    if service_type is None:
        if 'github' in site:
            service_type = 'github'
        elif 'bitbucket' in site or 'atlassian' in site:
            service_type = 'bitbucket'
        else:
            service_type = site

    if service_type == 'bitbucket':
        from git_cloner.bitbucket import BitbucketCloner
        BitbucketCloner(site, owner=owner, login=login, password=password).clone()
    elif service_type == 'github':
        from git_cloner.github import GithubCloner
        GithubCloner(site, owner=owner, login=login, password=password).clone()
    else:
        print('Unknown service provider type "{}"!'.format(service_type))
        exit(1)

