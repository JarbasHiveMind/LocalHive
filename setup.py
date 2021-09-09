from setuptools import setup

setup(
    name='HiveMind-LocalHive',
    version='0.0.2',
    packages=['local_hive',
              'local_hive.cli',
              'local_hive.skills',
              'local_hive.audio'],
    install_requires=["HolmesV[skills_minimal]>=2021.9.9",
                      "hivemind_bus_client>=0.0.2",
                      "jarbas_hive_mind>=0.10.3"],
    include_package_data=True,
    url='https://github.com/OpenJarbas/HiveMind-voice-sat',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='HiveMind skills runner',
    entry_points={
        'console_scripts': [
            'HiveMind-voice-sat=mycroft_voice_satellite.__main__:main'
        ]
    }
)
