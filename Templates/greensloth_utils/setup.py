from setuptools import setup, find_packages

setup(
    name="greensloth_utils",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    entry_points={
        "console_scripts": [
            "greensloth-install=greensloth_utils.installer:main",
        ],
    },
)
