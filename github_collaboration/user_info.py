''' Routines for getting user projects '''

from collections import namedtuple

import requests


_GITHUB_EVENT_URL = 'https://api.github.com/users/{username}/events'
_GITHUB_REPOS_URL = 'https://api.github.com/users/{username}/repos'
_GIHUB_REPOS_BY_OWNER_URL = 'https://api.github.com/repos/{owner}/{repo}'


RepositoryInfo = namedtuple("RepositoryInfo", ["id", "name"])


def _convert_params_to_auth_struct(auth_user, auth_password):
    if auth_user is not None or auth_password is not None:
        if auth_user is None or auth_user is None:
            raise ValueError(
                'auth_user and auth_password should be None simultaneously, got auth_user={auth_user} and auth_password={auth_password}'.format(
                    auth_user=auth_user, auth_password=auth_password
                )
            )
        auth_info = (auth_user, auth_password)
    else:
        auth_info = None

    return auth_info


def _get_user_events(username, auth_user=None, auth_password=None):
    auth_info = _convert_params_to_auth_struct(auth_user, auth_password)
    query = _GITHUB_EVENT_URL.format(username=username, auth=auth_info)
    all_events = requests.get(query, auth=auth_info)

    if all_events.status_code != 200:
        raise RuntimeError(all_events)

    return all_events.json()


def get_user_commits(username, auth_user=None, auth_password=None):
    all_events = _get_user_events(username, auth_user, auth_password)

    return [
        evet for evet in all_events
        if evet['type'] == 'PushEvent'
    ]


def get_user_repos(username, auth_user=None, auth_password=None):
    auth_info = _convert_params_to_auth_struct(auth_user, auth_password)

    query = _GITHUB_REPOS_URL.format(username=username)
    all_repos = requests.get(query, auth=auth_info)

    return all_repos.json()


def get_source_repo(owner, fork_id, auth_user=None, auth_password=None):
    auth_info = _convert_params_to_auth_struct(auth_user, auth_password)

    query = _GIHUB_REPOS_BY_OWNER_URL.format(owner=owner, repo=fork_id)
    repo = requests.get(query, auth_info)

    return repo.json()["parent"]


def get_user_base_repos(username, auth_user=None, auth_password=None):
    all_repos = get_user_repos(username, auth_user, auth_password)

    base_repos = []
    for repo in all_repos:
        if repo["fork"]:
            base_repo = get_source_repo(
                repo["owner"]['login'], repo["name"], auth_user, auth_password
            )

            base_repos.append(base_repo)
        else:
            base_repos.append(repo)

    return base_repos


def get_users_repos(usernames, auth_user=None, auth_password=None):
    return {
        user: get_user_base_repos(user, auth_user, auth_password)
        for user in usernames
    }
