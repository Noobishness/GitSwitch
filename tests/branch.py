import pytest
from typing import Tuple
from gitswitch.repository import Repository
from .helpers import get_dirs, get_repos

def test_has_remote(tmp_path):
    (local_repo, remote_repo) = get_repos(tmp_path)
    
    assert not remote_repo.has_remote(), 'Remote repo should only be local'
    assert local_repo.has_remote(), 'Local repo should have a remote'

def test_get_commit(tmp_path):
    (local_repo, remote_repo) = get_repos(tmp_path)
    local_master = remote_repo['master']
    remote_master = local_repo['master']

    assert local_master.get_commit().hexsha == remote_master.get_commit().hexsha