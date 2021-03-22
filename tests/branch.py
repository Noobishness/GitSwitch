from gitswitch.branch import get_all_branches
import pytest
from typing import Tuple
from gitswitch.repository import Repository

def test_has_remote(tmp_path):
    (local_repo, remote_repo) = get_repos(tmp_path)
    
    assert not remote_repo.has_remote(), 'Remote repo should only be local'
    assert local_repo.has_remote(), 'Local repo should have a remote'

def test_get_commit(tmp_path):
    (local_repo, remote_repo) = get_repos(tmp_path)
    local_branches = get_all_branches(local_repo)
    remote_branches = get_all_branches(remote_repo)

    local_master = remote_branches['master']
    remote_master = local_branches['master']

    assert local_master.get_commit().hexsha == remote_master.get_commit().hexsha

@pytest.mark.skip(reason="helper method")
def get_repos(tmp_path) -> Tuple[Repository, Repository]:
    local_path = tmp_path / 'local_repo'
    remote_path = tmp_path / 'remote_repo'

    clean_dir(local_path)
    clean_dir(remote_path)

    remote_repo = Repository(remote_path, None, False)
    local_repo = Repository(local_path, remote_path, False)

    return (local_repo, remote_repo)

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