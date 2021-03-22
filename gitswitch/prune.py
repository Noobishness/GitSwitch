from .branch import Branch
from .repository import Repository
from typing import List

"""
def analyze_merges(local_dir:str, remote_path:str , base_path: str, main_branch: str):
    repo = Repository(local_dir, remote_path)
    branches = branch.get_all_branches(repo)

    results = []
    main = branches[main_branch]
    for (name,data) in branches.items():
        if name.startswith(base_path) and name != main_branch:
            if main.contains(data):
                results.append(f'{name} OK')
            else:
                results.append(f'{name} Missing')
    return results
"""
