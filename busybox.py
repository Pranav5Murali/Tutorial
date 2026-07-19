import subprocess

IMAGE_ID = "c6348fa86ba0"

# Create container
result = subprocess.run(
    ["docker", "run", "-d", IMAGE_ID, "sh", "-c", "sleep 300"],
    capture_output=True,
    text=True,
    check=True
)

container_id = result.stdout.strip()

print(f"Container ID: {container_id}")

# Execute commands
subprocess.run(["docker", "exec", container_id, "pwd"], check=True)
subprocess.run(["docker", "exec", container_id, "ls"], check=True)

# Cleanup
#subprocess.run(["docker", "stop", container_id], check=True)
#subprocess.run(["docker", "rm", container_id], check=True)
