import os
import git


# 添加提交用户 邮箱
def git_user(repo_git, **user_info):
    for key in user_info:
        repo_git.config("--global", "user.{}".format(key), "%s" %(user_info[key]))


class Vault:
    def __init__(self, local_path, remote_path, username, email, vault_name='default', branch='main'):
        user_info = {'username': username, 'email': email}
        self.vault_name, self.local_path, self.remote_path, self.user_info, self.branch = \
            vault_name, local_path, remote_path, user_info, branch
        self.repo, self.repo_git, self.remote = self.init(
            vault_name, local_path, remote_path, user_info, branch=branch)

    def branch_exists(branch_name):
        for branch in repo.branches:
            if branch.name == branch_name:
                return True
        return False

    # 初始化vault
    def init(self, vault_name, local_path, remote_path, user_info, branch):
        vault_path = os.path.join(local_path)

        local_exists = lambda: os.path.exists(vault_path)
        remote_exists = lambda repo: repo is not None and repo.__class__ is git.Repo
        branch_exists = lambda repo, branch_name: branch_name in (branch.name for branch in repo.branches)

        if not local_exists():
            repo = git.Repo.clone_from(remote_path, to_path=vault_path, branch=branch)
            if not remote_exists(repo):
                os.makedirs(vault_path)
                repo = git.Repo.init(path=vault_path, branch=branch)
                remote = repo.create_remote('origin', remote_path)
            else:
                remote = repo.remotes[0]
        else:
            try:
                repo = git.Repo(vault_path)
            except git.exc.InvalidGitRepositoryError:
                dot_git = os.path.join(vault_path, '.git')
                if os.path.exists(dot_git):
                    os.rmdir(dot_git)
                repo = git.Repo.init(path=vault_path)


            if len(repo.remotes) == 0:
                remote = repo.create_remote('origin', remote_path)
            else:
                remote = repo.remotes[0]
            
            if remote.url != remote_path:
                remote.set_url(remote_path)

            
        repo_git = repo.git
        

        remote.fetch(refspec=f'refs/heads/{branch}:refs/remotes/{remote.name}/{branch}')
        if branch not in repo.branches:
            new_branch = repo.create_head(branch, remote.refs[branch])
            new_branch.checkout()
        else:
            local_branch = repo.branches[branch]
            local_branch.checkout()

        print(remote.refs)
        
        readme_path = os.path.join(vault_path, 'README.md')
        if not os.path.exists(readme_path):
            with open(remote_path, 'w') as f:
                f.write(f'# S-Note Vault {vault_name}\n---\nWelcome.\n')

        if repo.is_dirty():
            repo_git.add('-A')
            repo_git.commit('-m', 'auto commit')
        
        if not branch_exists(repo, branch):
            repo.create_head(branch)

        if repo.active_branch.name != branch:
            repo_git.checkout(branch)
            # repo.active_branch.set_tracking_branch(remote.refs[branch])
        git_user(repo_git, **user_info)

        remote.push(branch)
                
        print(remote)
        return repo, repo_git, remote


    def write(self, relative_path, content, commit_msg, **kwargs):
        vault_path = os.path.join(self.local_path, self.vault_name)

        file_dir_name = os.path.join(vault_path, os.path.dirname(relative_path))
        if not os.path.exists(file_dir_name):
            os.makedirs(file_dir_name)
        file_path = os.path.join(vault_path, relative_path)
        with open(file_path, 'w') as f:
            f.write(content)
        self.repo_git.add(relative_path)

        try:
            self.remote.fetch(refspec=f'refs/heads/{self.branch}:refs/remotes/{self.remote.name}/{self.branch}')
            if self.branch not in self.repo.branches:
                new_branch = self.repo.create_head(self.branch, self.remote.refs[self.branch])
                new_branch.checkout()
            else:
                local_branch = self.repo.branches[self.branch]
                local_branch.checkout()

            self.repo_git.add('-A')
            self.repo_git.commit('-m', commit_msg)

        except git.exc.GitCommandError as e:
            print(e)
        try:
            self.remote.push(self.branch)
        except git.exc.GitCommandError as e:
            print(e)
            

if __name__ == "__main__":
    vault_name = 'q1'
    local_path = r'C:\git_repos\test_vault_dir'
    remote_path = "http://192.168.4.200:8000/danim/{}.git"
    user_info = { 'name': 'danimeo', 'email': 'danimeon@outlook.com' }

    v = Vault(vault_name, local_path, remote_path, user_info, branch='master')

    branches = v.remote.refs
    for item in branches:
        print(item.remote_head)

    print(v.repo.refs, v.repo.head, v.repo.head.ref)

    # v.write('logs/med_logs.txt', '001 0832,0924 tmxt24,1 s?/7\n002 0832,2132 tmxt48,2 s?/7\n', 'log: took meds `tmxt24,1` `tmxt48,2`')

    v.write('logs/med_logs.txt', '001 0832,0924 tmxt25,1 s?/7\n002 0832,2132 tmxt10,2 s?/7\n003 ???\n', 'med_logger: changed logs `001` `002`')
