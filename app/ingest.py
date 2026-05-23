import os
import shutil
from git import Repo


def clone_repo(repo_url, save_base="data"):
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    save_path = os.path.join(save_base, repo_name)

    if os.path.exists(save_path):
        print("Repo already exists")
        return save_path

    os.makedirs(save_base, exist_ok=True)
    Repo.clone_from(repo_url, save_path)
    print("Repo cloned")

    return save_path


def load_code_files(repo_path, max_files=300):
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d for d in dirs
            if d not in [".git", "__pycache__", "node_modules", ".venv", "venv"]
        ]

        for file in files:
            if len(code_files) >= max_files:
                return code_files

            if file.endswith((".py", ".js", ".ts", ".java", ".go", ".cpp", ".md")):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code_files.append(f.read())
                except Exception:
                    continue

    return code_files


def chunk_code(code_files, chunk_size=500, max_chunks=2000):
    chunks = []

    for code in code_files:
        for i in range(0, len(code), chunk_size):
            chunks.append(code[i:i + chunk_size])

    return chunks


if __name__ == "__main__":
    repo = clone_repo("https://github.com/psf/requests")
    files = load_code_files(repo)
    chunks = chunk_code(files)

    print(f"Total chunks: {len(chunks)}")