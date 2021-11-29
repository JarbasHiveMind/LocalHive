from setuptools import setup

setup(
    name='HiveMind-LocalHive',
    version='0.0.3a1',
    packages=['local_hive'],
    install_requires=["hivemind_bus_client~=0.0.3a2",
                      "ovos-plugin-manager~=0.0.3a3",
                      "ovos-core[skills]~=0.0.2a1",
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
