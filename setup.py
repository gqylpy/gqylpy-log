import setuptools
import gqylpy_log as g

gdoc: list = g.__doc__.split("\n")

for index, line in enumerate(gdoc):
    if line.startswith("@version: ", 4):
        version = line.split()[-1]
        break
_, author, email = gdoc[index + 1].split()
source = gdoc[index + 2].split()[-1]

setuptools.setup(
    name=g.__name__,
    version=version,
    author=author,
    author_email=email,
    license="Apache 2.0",
    url="http://gqylpy.com",
    project_urls={"Source": source},
    description="""
        Secondary encapsulation `logging`, more convenient and fast to create
        the logger. Use this module can quickly create instances of
        `logging.Logger` and complete a series of log configuration, make your
        code cleaner.
    """.strip().replace('\n       ', ''),
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    packages=[g.__name__],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Artistic Software",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13"
    ]
)
