from typing import Tuple
import pytest
from gitswitch.repository import Repository

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