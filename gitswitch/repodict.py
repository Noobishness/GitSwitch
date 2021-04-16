from .repository import Repository
from .branch import Branch

class Repodict:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.branches = dict(str, Branch)

    def __getitem__(self, branch_name: str) -> Branch:
        if branch_name in self.branches:
            return self.branches[branch_name]
        return None
        
    def actualize(self):
        self.repo.fetch()
        if self.repo.has_remote():
            for remote in self.repo.remote_branches:
                name = remote.name[len('origin/'):]
                if name != 'HEAD':
                    if not name in self.branches:
                        self.branches[name] = Branch(self, name)
                    else:
                        self.branches[name].remote_branch = remote
        for local in self.repo.local_branches:
            if not local.name in self.branches:
                self.branches[local.name] = Branch(self, local.name)
            else:
                self.branches[local.name].local_branch = local
