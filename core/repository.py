from git import Repo, InvalidGitRepositoryError, GitCommandError
import os
from os import path
from typing import List

class Repository:
    def __init__(self, local_dir: str, remote_url: str):
        assert local_dir, "local dir is empty"
        self.local_dir = local_dir
        self.remote_url = remote_url
        self.actualize()

    def actualize(self):
        self.ensure_cloned()
        self.fetch()

    def checkout(self, branch_name: str):
        self.repo.git.checkout(branch_name)
    
    def ensure_cloned(self):
        if not path.exists(self.local_dir):
            os.makedirs(self.local_dir)
        if self.remote_url:
            try:
                self.repo = Repo(self.local_dir)
            except InvalidGitRepositoryError:
                self.clone()
    
    def clone(self):
        assert self.remote_url, "Remote url is empty"
        self.repo = Repo.clone_from(self.remote_url, self.local_dir)

    def fetch(self):
        for remote in self.repo.remotes:
            remote.fetch()
        self.remote_branches = self.repo.remote().refs
        self.local_branches = self.repo.heads

    def merge(self, to_branch: str, from_branch: str) -> bool:
        base = self.repo.merge_base(to_branch, from_branch)
        try:
            self.repo.repo.index.merge_tree(to_branch, base=base)
        except GitCommandError:
            return False

    def get_merge_base(self, to_branch_sha: str, from_branch_sha: str) -> str:
        return self.repo.git.execute(['git', 'merge-base', to_branch_sha, from_branch_sha])