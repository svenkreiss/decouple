from distutils.core import setup
 
setup(
    name='Decouple',
    version='1.1.0',
    packages=['Decouple', 'Decouple.src', 'Decouple.src.LHCXSHiggsCouplings'],
    license='LICENSE',
    description='Decouple and recouple.',
    long_description=open('README.md').read(),
    author='Sven Kreiss, Kyle Cranmer',
    author_email='sk@svenkreiss.com',

    dependency_links= [
        'https://github.com/svenkreiss/BatchLikelihoodScan/tarball/master#egg=BatchLikelihoodScan-1.0.2',
    ],
    install_requires= ['BatchLikelihoodScan','numpy','scipy','multiprocessing','progressbar'],

    entry_points={
        'console_scripts': [
            'decouple = Decouple.decouple:main',
            'recouple = Decouple.recouple:main',

            # decouple tools
            'decouple_obtain_etas = Decouple.src.obtainEtas:main',

            # recouple tools
            'recouple_mutmuw = Decouple.src.muTmuW:main',
            'recouple_kvkf = Decouple.src.kVkF:main',
            'recouple_kglukgamma = Decouple.src.kGlukGamma:main',
        ]
    }
)
