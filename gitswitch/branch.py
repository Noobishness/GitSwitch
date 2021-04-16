from typing import Dict, List
from git import Commit, GitCommandError

from .repository import Repository

class Branch:
    def __init__(self, repo: Repository, name: str):
        self.name = name
        self.repo = repo
        try:
            self.local_branch = self.repo.local_branches[name]
        except IndexError:
            self.local_branch = None
        if self.repo.has_remote():
            try:
                self.remote_branch = self.repo.remote_branches[name]
            except IndexError:
                self.remote_branch = None
        else:
            self.remote_branch = None

    def activate(self):
        self.repo.checkout(self.name)

    def is_local(self) -> bool:
        return self.local_branch is not None

    def is_remote(self) -> bool:
        return self.remote_branch is not None

    def get_commit(self) -> Commit:
        try:
            if self.is_remote():
                return self.remote_branch.commit
            else:
                return self.local_branch.commit
        except Exception as ex:
            raise Exception(f'failed to retrieve branch of {self.name} due to {ex}')

    def is_merged_into(self, target_branches: List['Branch']) -> bool:
        for target_branch in target_branches:
            if target_branch.contains(self):
                return True
        return False

    def contains(self, source_branch: 'Branch') -> bool:
        merge_base = self.get_merge_base(source_branch)
        return merge_base == source_branch.get_commit().hexsha

    def get_merge_base(self, source_branch: 'Branch') -> str:
        return self.repo.get_merge_base(self.get_commit().hexsha, source_branch.get_commit().hexsha)

    def merge_into(self, target_branch: 'Branch') -> bool:
        target_branch.activate()
        base = self.repo.repo.merge_base(target_branch, self.name)
        try:
            self.repo.repo.index.merge_tree(target_branch.name, base=base)
        except GitCommandError:
            return False
        self.repo.repo.index.commit(f'Merge {self.name} into {target_branch.name}', parent_commits=(target_branch.get_commit(), self.get_commit()))
        self.repo.actualize()
        return True

    