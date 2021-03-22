
from git.repo.base import Repo

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

@pytest.mark.skip(reason="helper method")
def get_dirs(tmp_path) -> Tuple[str, str]:
    local_path = tmp_path / 'local_repo'
    remote_path = tmp_path / 'remote_repo'

    clean_dir(local_path)
    clean_dir(remote_path)

    return (local_path, remote_path)

@pytest.mark.skip(reason="helper method")
def clean_dir(curr_path):
    import os
    import shutil

    if not os.path.exists(curr_path):
        os.makedirs(curr_path)
    else:
        for root, dirs, files in os.walk(curr_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))