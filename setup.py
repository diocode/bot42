from setuptools import setup, find_packages

setup(
  name="LookinSlack",
  version="0.1.0",
  description="Get Piscine & Student progress data",
  author="passunca & digoncal",
  packages=find_packages(where="app"),
  package_dir={"": "app"},
  install_requires=[
    "setuptools", 
    "slack_bolt",
    "requests", 
  ],
  extras_require={
    "dev": ["debugpy", "black"],
  },
)
