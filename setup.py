"""
Setup script for ifm ZZ1350 IO-Link Master Python library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="ifm-zz1350-iolink-python",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python library for ifm AL1350 IO-Link Master communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ifm-zz1350-iolink-python",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Hardware",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "requests-mock>=1.9.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "iolink-scan=examples.quick_scanner:main",
            "iolink-monitor=examples.temperature_monitor:main",
            "iolink-discover=scripts.network_discovery:main",
        ],
    },
    keywords="iolink, ifm, industrial, iot, automation, sensors, temperature",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ifm-zz1350-iolink-python/issues",
        "Source": "https://github.com/yourusername/ifm-zz1350-iolink-python",
        "Documentation": "https://github.com/yourusername/ifm-zz1350-iolink-python/blob/main/docs/API.md",
        "Article": "YOUR_LINKEDIN_ARTICLE_URL",
    },
)
