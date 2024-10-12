import configparser
import subprocess

def get_api_key(config_file="config.ini.enc"):
    """Decrypts the config file and returns the API key."""
    try:
        # Decrypt the config file (you'll need to enter the password)
        subprocess.run(
            [
                "openssl",
                "aes-256-cbc",
                "-d",
                "-salt",
                "-in",
                config_file,
                "-out",
                "config.ini",
            ],
            check=True,
        )
        # Read the API key from the decrypted file
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config["gemini"]["api_key"]
    except Exception as e:
        print(f"Error reading API key: {e}")
        return None