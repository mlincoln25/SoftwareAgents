import subprocess

def commit_and_push(message):
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        return 'Code committed and pushed successfully.'
    except subprocess.CalledProcessError as e:
        return f'Error during commit/push: {e}'

# Example usage:
# print(commit_and_push("Initial commit"))
