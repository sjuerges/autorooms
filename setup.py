from setuptools import setup, find_packages

requirements = ("aiohttp>=3.3.0,<3.4.0", "websockets>=6.0,<7.0", "discord.py>=1.0.0a")

dependency_links = (
    "https://github.com/Rapptz/discord.py/"
    "archive/8ccb98d395537b1c9acc187e1647dfdd07bb831b.tar.gz#egg=discord.py-1.0.0a0",
)


def get_package_list():
    return find_packages(include=["autorooms", "autorooms.*"])


if __name__ == "__main__":
    setup(
        name="discord-autorooms",
        version="2.1.3",
        packages=get_package_list(),
        url="https://github.com/mikeshardmind/autorooms",
        license="MIT",
        author="mikeshardmind",
        author_email="",
        description="Zero Config Autoroom Discord Bot",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Framework :: AsyncIO",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Communications :: Chat",
            "Natural Language :: English",
        ],
        entry_points={"console_scripts": ["discord-autorooms=autorooms.__main__:main"]},
        python_requires=">=3.6,<3.8",
        dependency_links=dependency_links,
        install_requires=requirements,
    )
