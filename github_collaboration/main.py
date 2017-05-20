import argparse

import matplotlib.pyplot as plt

import user_info
import bipartite_utils


_helps = {
    "login": "login for authentificatoin",
    "password": "password for authentificatoin",
    "login-file": "path to file with logins"
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", default=None, help=_helps["login"])
    parser.add_argument("--password", default=None, help=_helps["password"])
    parser.add_argument("--login-file", help=_helps["login-file"])

    return parser.parse_args()


def read_logins_from_file(filepath):
    with open(filepath, "r") as inp:
        logins = [s.strip() for s in inp]

    return logins


def main():
    args = parse_args()

    logins = read_logins_from_file(args.login_file)
    info = user_info.get_users_repos(logins)

    g = bipartite_utils.create_graph_from_user_info(info)

    bipartite_utils.show_graph(g)
    plt.show()

if __name__ == "__main__":
    main()
