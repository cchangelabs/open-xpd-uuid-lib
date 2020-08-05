from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='open-xpd-uuid',
    version='0.2.0',
    description='A library of common functions used when creating and managing open-xpd-uuid, '
                'a common, globally-unique name space (uuid) for Product Declarations, including HPDs and EPDs, '
                'to help users find all environmental and health information related to a single product.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='C-Change Labs',
    maintainer_email='open-source@c-change-labs.com',
    url='https://github.com/cchangelabs/open-xpd-uuid-lib',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    tests_require=['pytest'],
)
