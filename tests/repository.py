
from git.repo.base import Repo
from .helpers import get_dirs

import pytest
from typing import Tuple

def test_local_detection(tmp_path):
    from gitswitch.repository import Repository

    (local_path, _) = get_dirs(tmp_path)
    repo = Repository(local_path, None, True)

    assert not repo.has_remote(), 'Repo has no remote path but reports to have one'

def test_init(tmp_path):
    from git import Repo
    from gitswitch.repository import Repository
    from os import path

    (local_path, _) = get_dirs(tmp_path)
    repo = Repository(local_path, None, True)
    repo.init()

    assert path.exists(local_path), 'Path should at least exist'
    Repo(local_path) # will throw if it is no valid git repo

def test_fetch_remote(tmp_path):
    from git import Repo
    from gitswitch.repository import Repository
    from os import path

    (local_path, remote_path) = get_dirs(tmp_path)
    Repository(remote_path, None, False)
    Repository(local_path, remote_path, False)

    assert path.exists(local_path), 'Path should at least exist'
    Repo(local_path) # will throw if it is no valid git repo