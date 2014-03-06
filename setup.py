from distutils.core import setup
 
setup(
    name='Decouple',
    version='1.2.4',
    packages=['Decouple', 'Decouple.BatchPlugins', 'scripts'],
    license='LICENSE',
    description='Decouple and recouple.',
    long_description=open('README.md').read(),
    author='Sven Kreiss, Kyle Cranmer',
    author_email='sk@svenkreiss.com',

    install_requires= [
        'BatchLikelihoodScan',
        'LHCHiggsCouplings',
        'numpy',
        'scipy',
        'multiprocessing',
        'progressbar',
    ],

    entry_points={
        'console_scripts': [
            'decouple = scripts.decouple:main',
            'recouple = scripts.recouple:main',

            # decouple tools
            'decouple_obtain_etas = Decouple.obtainEtas:main',

            # recouple tools
            'recouple_mutmuw = Decouple.muTmuW:main',
            'recouple_kvkf = Decouple.kVkF:main',
            'recouple_kglukgamma = Decouple.kGlukGamma:main',
        ]
    }
)
