from setuptools import setup, find_packages

setup(
  name="LookinSlack",
  version="0.1.0",
  description="A short description of the project",
  author="passunca & digoncal",
  packages=find_packages(where="app"),
  package_dir={"": "app"},
  install_requires=[
    "requests", 
    "setuptools", 
    "slack_bolt",
  ],
  extras_require={
    "dev": ["debugpy", "black"],
  },
)
