import os
from dotenv import load_dotenv
from langchain_community.document_loaders import GithubFileLoader

load_dotenv()

def sync_from_github():
    print("🌐 Connecting to GitHub...")
    loader = GithubFileLoader(
        repo="awsdocs/amazon-s3-developer-guide", # Change to any AWS repo
        branch="master",
        access_token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        file_filter=lambda file_path: file_path.endswith(".md")
    )

    documents = loader.load()
    output_folder = "./aws_knowledge_base"
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    
    for doc in documents:
        filename = doc.metadata['file_path'].replace("/", "_")
        with open(os.path.join(output_folder, filename), "w", encoding="utf-8") as f:
            f.write(doc.page_content)
    print(f"✅ Synced {len(documents)} files.")