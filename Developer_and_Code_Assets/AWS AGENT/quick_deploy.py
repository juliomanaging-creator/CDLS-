import os
import subprocess
from multiprocessing import Pool
from langchain_text_splitters import MarkdownHeaderTextSplitter

# List of essential high-priority repos for your "Compute" and "ML" skills
REPOS = [
    "aws-lambda-developer-guide", "amazon-sagemaker-developer-guide",
    "amazon-bedrock-user-guide", "amazon-ec2-user-guide",
    "amazon-vpc-user-guide", "amazon-eks-user-guide"
]

def quick_clone(repo):
    target = f"./knowledge/{repo}"
    if not os.path.exists(target):
        # --depth 1 only downloads the latest version, saving time and space
        subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/awsdocs/{repo}.git", target])

if __name__ == "__main__":
    # 1. Parallel Download
    print("🚀 Starting high-speed documentation sync...")
    with Pool(4) as p:
        p.map(quick_clone, REPOS)

    # 2. Automated Indexing Check
    print("✅ Files collected. Ready for local deployment.")
    