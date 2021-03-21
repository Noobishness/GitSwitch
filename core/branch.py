from typing import Dict, List

from repository import Repository


class Branch:
    def __init__(self, repo: Repository, name: str):
        self.name = name
        self.repo = repo
        try:
            self.local_branch = self.repo.local_branches[name]
        except IndexError:
            self.local_branch = None
        try:
            self.remote_branch = self.repo.remote_branches[name]
        except IndexError:
            self.remote_branch = None

    def activate(self):
        self.repo.checkout(self.name)

    def is_local(self) -> bool:
        return self.local_branch is not None

    def is_remote(self) -> bool:
        return self.remote_branch is not None

    def get_commit(self):
        try:
            if self.is_remote():
                return self.remote_branch.commit
            else:
                return self.local_branch.commit
        except Exception as ex:
            raise Exception(f'failed to retrieve branch of {self.name} due to {ex}')

    def is_merged_into(self, target_branches: List['__class__']) -> bool:
        for target_branch in target_branches:
            if target_branch.contains(self):
                return True
        return False

    def contains(self, source_branch: '__class__') -> bool:
        merge_base = self.get_merge_base(source_branch)
        return merge_base == source_branch.get_commit().hexsha

    def get_merge_base(self, source_branch: '__class__') -> str:
        return self.repo.get_merge_base(self.get_commit().hexsha, source_branch.get_commit().hexsha)

def get_all_branches(repo: Repository) -> Dict[str, Branch]:
    branches = dict()
    for remote in repo.remote_branches:
        name = remote.name[len('origin/'):]
        if name != 'HEAD':
            branches[name] = Branch(repo, name)
    for local in repo.local_branches:
        if not local.name in branches:
            branches[local.name] = Branch(repo, local.name)
    return branches
