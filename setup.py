from setuptools import setup, find_packages


setup(
    name='playmusic-downloader.py',
    version='0.1',
    url='https://github.com/dr1s/playmusic-downloader.py',
    author='drs',
    license='MIT',
    description='Download all your songs from Google Play Music',
    install_requires=["eyed3", "gmusicapi"],
    packages=find_packages(),
    entry_points={'console_scripts': ['playmusicdl=playmusicdl.playmusicdl:main']},
)
