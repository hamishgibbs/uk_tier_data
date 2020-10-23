import setuptools

setuptools.setup(
    name="uk_tier_data",
    version="0.0.1",
    author="Hamish Gibbs",
    author_email="Hamish.Gibbs@lshtm.ac.uk",
    description="Scrape UK Tier data from Wikipedia.",
    url="https://github.com/hamishgibbs/uk_tier_data",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
