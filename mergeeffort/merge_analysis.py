from pygit2 import *
import os
import shutil
import argparse
import time


def get_actions(diff_a_b):
	actions = set()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				aux = (file_name, l.content, l.origin)
				actions.add(aux)

	return actions

def clone(url):
	repo_url = url
	current_working_directory = os.getcwd()
	repo_path = current_working_directory + "/" + str(time.time())
	repo = clone_repository(repo_url, repo_path) 

	return repo


def calculate_rework(parent1_actions, parent2_actions, parents_actions):
	rework_actions = set(parent1_actions).intersection(parent2_actions)
	rework_actions_relative = '{:.0%}'.format(len(rework_actions) / len(parents_actions))
	rework_actions_absolute = len(rework_actions)

	return [rework_actions_relative, rework_actions_absolute]

def calculate_no_effort(merge_actions, parents_actions):
	no_effort = merge_actions.intersection(parents_actions)
	no_effort_relative = '{:.0%}'.format(len(no_effort) / len(merge_actions))
	no_effort_absolute = len(no_effort)

	return [no_effort_relative, no_effort_absolute]

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions
	wasted_actions_relative = '{:.0%}'.format(len(wasted_actions) / len(parents_actions))
	wasted_actions_absolute = len(wasted_actions)
	return [wasted_actions_relative, wasted_actions_absolute]

def calculate_additional_effort(merge_actions, parents_actions):
	additional_actions = merge_actions - parents_actions
	additional_actions_relative = '{:.0%}'.format(len(additional_actions) / len(merge_actions))
	additional_actions_absolute = len(additional_actions)
	
	return [additional_actions_relative, additional_actions_absolute]


def analyse(commits, repo):
	commits_metrics = {}
	for commit in commits:
		if (len(commit.parents)==2):
			parent1 = commit.parents[0]
			parent2 = commit.parents[1]

			base = repo.merge_base(parent1.hex, parent2.hex)
			base_version = repo.get(base)
			
			diff_base_final = repo.diff(base_version, commit, context_lines=0)
			diff_base_parent1 = repo.diff(base_version, parent1, context_lines=0)
			diff_base_parent2 = repo.diff(base_version, parent2, context_lines=0)

			merge_actions = get_actions(diff_base_final)
			parent1_actions = get_actions(diff_base_parent1)
			parent2_actions = get_actions(diff_base_parent2)

			commits_metrics[commit.hex] = calculate_metrics(merge_actions, parent1_actions, parent2_actions)

	return commits_metrics	


def calculate_metrics(merge_actions, parent1_actions, parent2_actions):	
	metrics = {}

	parents_actions = set(parent1_actions).union(parent2_actions)

	rework = calculate_rework(parent1_actions, parent2_actions, parents_actions)
	metrics['Parents rework - relative'] = rework[0]
	metrics['Parents rework - absolute'] = rework[1]

	wasted = calculate_wasted_effort(parents_actions, merge_actions)
	metrics['Wasted actions - relative'] = wasted[0]
	metrics['Wasted actions - absolute'] = wasted[1]

	additional = calculate_additional_effort(merge_actions, parents_actions)
	metrics['Additional actions - relative'] = additional[0]
	metrics['Additional actions - absolute'] = additional[1]


	no_effort = calculate_no_effort(merge_actions, parents_actions)
	metrics['No effort actions - relative'] = no_effort[0]
	metrics['No effort actions - absolute'] = no_effort[1]

	return metrics

			
def main():
	#local - /Users/tayanemoura/Documents/git/teste_merge
	#url - 'git://github.com/tayanemoura/teste_merge.git'
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--url", help="set an url for a git repository")
	group.add_argument("--local", help="set the path of a local git repository")
	parser.add_argument("--commit", nargs='+', help="set the commit (or a list of commits separated by comma) to analyse. Default: all merge commits")
	args = parser.parse_args()

	if args.url:
		repo = clone(args.url) 

	elif args.local:
		repo = Repository(args.local)

	commits = []
	if args.commit:
		for commit in args.commit:
			commits.append(repo.get(commit))

	else:
		commits = repo.walk(repo.head.target, GIT_SORT_TIME | GIT_SORT_REVERSE)

	commits_metrics = analyse(commits, repo)
	print(commits_metrics)

	if args.url:
		shutil.rmtree(repo.workdir)

	
if __name__ == '__main__':
	main()	

