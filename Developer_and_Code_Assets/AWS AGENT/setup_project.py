import os

def create_project_structure():
    # Define the main folders
    folders = [
        "aws_knowledge_base",    # Where you put your .md files
        "faiss_aws_index",       # Where the searchable database lives
        "scripts",               # Optional: For backup scripts
    ]

    print("🛠️  Initializing AWS Agent Project...")

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Created folder: {folder}")
        else:
            print(f"ℹ️  Folder already exists: {folder}")

    # Create a dummy file in the knowledge base so the indexer doesn't crash
    dummy_file = os.path.join("aws_knowledge_base", "example_service.md")
    if not os.path.exists(dummy_file):
        with open(dummy_file, "w") as f:
            f.write("# Example AWS Service\nThis is a placeholder for your AWS documentation.")
        print(f"📝 Created dummy doc: {dummy_file}")

    print("\n🚀 Project structure is ready!")
    print("Next Step: Put your actual AWS .md files into 'aws_knowledge_base'.")

if __name__ == "__main__":
    create_project_structure()
    