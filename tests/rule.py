import pytest
from typing import Tuple
from gitswitch.repository import Repository
from .helpers import get_dirs, get_repos
from gitswitch.rule import MergeForwardRule

def test_merge_direct(tmp_path):
    (_, remote_repo) = get_repos(tmp_path)
    remote_master = remote_repo['master']

    #create a second branch which is ahead of master
    remote_repo.create_branch('test', remote_master.get_commit().hexsha)
    remote_repo.write_and_commit("test.txt", "dummy commit", "dummy1")

    remote_master = remote_repo['master']
    remote_test= remote_repo['test']

    assert remote_master.contains(remote_test)
    assert not remote_test.contains(remote_master)

    rule = MergeForwardRule(remote_repo, remote_master, remote_test, False, True, None)

    assert rule.try_merge(), 'merge should work'
    
    remote_master = remote_repo['master']
    remote_test= remote_repo['test']

    assert remote_test.contains(remote_master)


