from setuptools import setup, find_namespace_packages

setup(name="pinyin",
      version="0.1",
      description="Convert Chinese character to pinyin",
      url="https://github.com/xungongmichael/pinyin",
      author="Michael Gong",
      license="MIT",
      packages=find_namespace_packages(where="pinyin"),
      package_dir={"": "pinyin"},
      package_data={
          "pinyin": ["*.json"],
      },
      zip_safe=False,
      include_package_data=True)
