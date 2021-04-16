from git import Repo, InvalidGitRepositoryError, GitCommandError
import os
from os import path
from .branch import Branch
from typing import Dict

class Repository:
    def __init__(self, local_dir: str, remote_url: str, no_actualize: bool):
        assert local_dir, "local dir is empty"
        self.local_dir = local_dir
        self.remote_url = remote_url
        self.initiated = False
        if not no_actualize:
            self.actualize()

    def actualize(self):
        if self.has_remote():
            self.ensure_cloned()
            self.fetch()
        else:
            self.ensure_init()

    def has_remote(self) -> bool:
        return self.remote_url is not None

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
    
    def ensure_init(self):
        if not path.exists(self.local_dir):
            os.makedirs(self.local_dir)
        try:
            self.repo = Repo(self.local_dir)
        except InvalidGitRepositoryError:
            self.init()

    def clone(self):
        assert self.remote_url, "Remote url is empty"
        self.repo = Repo.clone_from(self.remote_url, self.local_dir)
        
    def init(self):
        if not path.exists(self.local_dir):
            os.makedirs(self.local_dir)
        if not self.initiated:
            self.repo = Repo.init(self.local_dir)
            self.write_and_commit('readme.md','init','init')
            self.initiated = True

    def create_branch(self, branch: str, commit_sha: str):
        self.repo.create_head(branch, commit_sha)

    def write_and_commit(self, file_name: str, commit: str, content: str):
        f = open(self.local_dir / file_name, "a")
        f.write(content)
        f.close()
        self.repo.index.add(file_name)
        self.repo.index.commit(commit)

    def fetch(self):
        if self.has_remote():
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