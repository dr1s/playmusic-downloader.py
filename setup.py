from setuptools import setup, find_packages


setup(
    name='playmusicdl',
    version='0.1',
    url='https://github.com/dr1s/playmusicdl.py',
    author='drs',
    license='MIT',
    description='Download all your songs from Google Play Music',
    install_requires=["eyed3", "gmusicapi"],
    packages=find_packages(),
    include_package_data = True,
    package_data = {
            '': ['genre_ids.json']
        },
    entry_points={'console_scripts': ['playmusicdl=playmusicdl.playmusicdl:main']},
)
