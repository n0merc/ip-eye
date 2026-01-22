from setuptools import setup

setup(
    name="ip-eye",
    version="1.0.0",
    author="n0merc",
    description="OSINT-based IP tracking and reconnaissance tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/n0merc/ip-eye",
    py_modules=["ip_eye"],
    install_requires=[
        "requests",
        "colorama",
        "dnspython",
        "python-whois",
        "shodan"
    ],
    entry_points={
        "console_scripts": [
            "ip-eye=ip_eye:main"
        ]
    },
    python_requires=">=3.8",
)
