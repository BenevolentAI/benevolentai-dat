from setuptools import setup, find_packages

setup(
    name="diversity_analysis_tool",
    description="Characterizing diversity in biodata and producing visualizations",
    version="0.0.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "assess_diversity = diversity_analysis_tool.cli:main"
        ]
    },
    test_suite="tests",
    python_requires=">=3.5",
    install_requires=[
        "pandas==1.1.0",
        "seaborn==0.10.1",
        "matplotlib==3.3.0",
    ]
)
