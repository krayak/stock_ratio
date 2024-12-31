from setuptools import setup, find_packages

setup(
    name='stock_ratios',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'yfinance',
    ],
    entry_points={
        'console_scripts': [
            'stock-ratios=stock_ratios.cli:main',  # This will point to the CLI entry point
        ],
    },
)
