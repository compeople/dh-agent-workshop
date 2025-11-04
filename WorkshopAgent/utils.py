import subprocess

def get_gcloud_access_token():
    try:
        token = (
            subprocess.check_output(["gcloud", "auth", "print-identity-token"])
            .strip()
            .decode("utf-8")
        )
        print(token)
        return token
    except subprocess.CalledProcessError as e:
        print(
            f"Error getting gcloud access token: {e}",
        )
        return None