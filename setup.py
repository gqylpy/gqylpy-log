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
    description="二次封装 logging，更方便快捷的创建日志记录器。使用 gqylpy_log 模块可以"
                "快速创建 logging.Logger 实例并完成一系列的日志配置，使你的代码更简洁。",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    packages=[g.__name__],
    python_requires=">=3.8, <4",
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
        "Programming Language :: Python :: 3.12"
    ]
)
