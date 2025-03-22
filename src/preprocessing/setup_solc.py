"""
Install and configure the Solidity compiler.
"""
import solcx

#latest version is 0.8.29 | Check what is different between this and version - 0.8.17
def setup_solc(version="0.8.29"):
    """Install and set the Solidity compiler version."""
    print(f"Installing solc version {version}...")
    solcx.install_solc(version)
    solcx.set_solc_version(version)
    print(f"Solc {version} installed and set as default")

if __name__ == "__main__":
    setup_solc()