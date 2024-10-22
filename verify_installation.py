# Test script to verify installations
import sys


def verify_installations():
    required_packages = [
        'networkx',
        'pandas',
        'numpy',
        'matplotlib',
        'lxml'
    ]

    missing_packages = []
    installed_versions = {}

    for package in required_packages:
        try:
            module = __import__(package)
            installed_versions[package] = getattr(module, '__version__', 'unknown')
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("\nMissing packages:")
        for package in missing_packages:
            print(f"- {package}")
        print("\nPlease install missing packages using:")
        print(f"pip install {' '.join(missing_packages)}")
    else:
        print("\nAll required packages are installed:")
        for package, version in installed_versions.items():
            print(f"- {package}: {version}")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    verify_installations()
