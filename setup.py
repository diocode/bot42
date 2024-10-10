from setuptools import setup, find_packages

setup(
    name="LookinSlack",
    version="0.1.0",
    description="Get Piscine & Student progress data",
    author="passunca & digoncal",
    package_dir={"": "app"},
    packages=find_packages(include=["app.*"]),
    include_package_data=True,
    scripts=["build.sh"],
    install_requires=[
        "setuptools",
        "slack_bolt",
        "requests",
    ],
    extras_require={
        "dev": ["debugpy", "black"],
    },
    data_files=[("scripts", ["build.sh"])],
)
