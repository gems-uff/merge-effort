import setuptools
setuptools.setup(
	name='merge-effort',    
	version='1.0',
	license='MIT',
	url='https://github.com/gems-uff/merge-effort',
	author='Tayane Moura and Leonardo Murta',
	author_email='tayanemoura@id.uff.br',
	description='a script to measure merge effort',
	packages= setuptools.find_packages(),
	entry_points={
		'console_scripts':[ 'merge-effort = mergeeffort.merge_analysis:main' ]
	},
	install_requires=[
        "pygit2>=0.27.0"
    ],

	)