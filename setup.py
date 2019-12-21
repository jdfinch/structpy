import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='structpy',
     version='0.2',
     scripts=[],
     author="James Finch",
     author_email="jdfinch@emory.edu",
     description="Graph algorithms and data structures",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/jdfinch/structpy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )

