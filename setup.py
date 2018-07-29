import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipython_slack_frontend",
    version="0.0.1",
    author="Pravendra Singh",
    author_email="hackpravj@gmail.com",
    description="IPython frontend that runs in Slack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pravj/ipython_slack_frontend",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)