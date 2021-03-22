import typing

from git import GitCommandError

from .branch import Branch
from .repository import Repository


class MergeForwardRule:
    internal_rules = []

    def __init__(self, repo: Repository, from_branch: Branch, to_branch: Branch, automerge: bool, autorepair: bool, merge_branch: str):
        self.repo = repo
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.automerge = automerge
        self.autorepair = autorepair
        self.merge_branch = merge_branch
        if merge_branch:
            real_merge_branch = repo.remote_branches[merge_branch]
            merge_from_source = MergeForwardRule(repo, self.from_branch, real_merge_branch, True, False, None)
            merge_to_source = MergeForwardRule(repo, real_merge_branch, self.to_branch, False, True, None)
            self.internal_rules.append(merge_from_source)
            self.internal_rules.append(merge_to_source)

    def is_merged(self) -> bool:
        return self.from_branch.is_merged_into([self.to_branch])

    def is_broken(self) -> bool:
        return not self.to_branch.is_merged_into([self.from_branch])

    def try_merge(self) -> bool:
        if self.is_merged():
            return True
        if self.merge_branch:
            return self.try_merge_indirect()
        else:
            return self.try_merge_direct()

    def try_merge_direct(self) -> bool:
        self.to_branch.activate()
        base = self.repo.repo.merge_base(self.to_branch.name, self.from_branch.name)
        try:
            self.repo.repo.index.merge_tree(self.to_branch.name, base=base)
        except GitCommandError:
            return False
        self.repo.repo.index.commit('Merge main into feature', parent_commits=(self.to_branch.get_commit().commit, self.from_branch.get_commit().commit))
        return True
    
    def try_merge_indirect(self) -> bool:
        success = True
        for subrule in self.internal_rules:
            if not subrule.sync():
                success = False
        return success

    def try_repair(self) -> bool:
        if not self.is_broken():
            return True
        self.from_branch.activate()
        base = self.repo.repo.merge_base(self.to_branch.name, self.from_branch.name)
        try:
            self.repo.repo.index.merge_tree(self.from_branch.name, base=base)
        except GitCommandError:
            return False
        self.repo.repo.index.commit(f'Reverse merge {self.to_branch.name} into {self.from_branch.name}', parent_commits=(self.to_branch.get_commit(), self.from_branch.get_commit()))
        return True

    def sync(self) -> bool:
        if self.autorepair:
            if not self.try_repair():
                return False
        if self.automerge:
            return self.try_merge()