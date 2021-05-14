import git
import os

git.Git("/your/directory/to/clone").clone("git://gitorious.org/git-python/mainline.git")

os.system(f"chmod +x uacs/uacs")

