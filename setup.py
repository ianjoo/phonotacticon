from setuptools import setup


setup(
    name='cldfbench_Phonotacticon',
    py_modules=['cldfbench_Phonotacticon'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'Phonotacticon=cldfbench_Phonotacticon:Dataset',
        ]
    },
    install_requires=[
        'cldfbench', 'pyglottolog',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
