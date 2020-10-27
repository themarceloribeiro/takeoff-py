import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="takeoff-py",
    scripts=['takeoff-generate'],
    version="0.0.5",
    author="Marcelo Ribeiro",
    author_email="themarceloribeiro@gmail.com",
    description="A Python toolset to launch full stack, mobile projects",
    long_description="A Python toolset to launch full stack, mobile projects. TakeOff helps you create the backend, frontend and client applications using native iOS/Android",
    long_description_content_type="text/markdown",
    url="https://github.com/themarceloribeiro/takeoff-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jinja2',
        'django-bootstrap4',
        'nose',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],    
    python_requires='>=3.6',
)