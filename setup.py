from setuptools import setup

setup(name="xorcrypt",
      version="0.2",
      description="Simple encryption software",
      long_description="README",
      long_description_content_type="text/markdown",
      url="http://github.com/tlapka06/xorcrypt",
      author="RTranscriptase",
      author_email="mail.me@anidor.org",
      license="MIT",
      packages=["xorcrypt"],
      include_package_data=True,
      install_requires=[
            "typing", "argparse"
      ],
      entry_points={"console_scripts": ["xorcrypt=xorcrypt:main"]})