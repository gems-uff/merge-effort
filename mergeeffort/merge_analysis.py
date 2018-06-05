from datetime import datetime
startTime = datetime.now()

from pygit2 import *
import os
import shutil
import argparse
import time
import traceback


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
	repo_path = current_working_directory + "/build/" + str(time.time())
	repo = clone_repository(repo_url, repo_path) 

	return repo


def calculate_rework(parent1_actions, parent2_actions, parents_actions):
	rework_actions = set(parent1_actions).intersection(parent2_actions)
	rework_actions= len(rework_actions)
	return rework_actions

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions
	wasted_actions = len(wasted_actions)
	return wasted_actions

def calculate_additional_effort(merge_actions, parents_actions):
	additional_actions = merge_actions - parents_actions
	additional_actions = len(additional_actions)
	return additional_actions


def analyse(commits, repo, detailed=False):
	commits_metrics = {}
	try:
		for commit in commits:
			if (len(commit.parents)==2):
				parent1 = commit.parents[0]
				parent2 = commit.parents[1]
				base = repo.merge_base(parent1.hex, parent2.hex)
				if(base): 
					base_version = repo.get(base)
					
					diff_base_final = repo.diff(base_version, commit, context_lines=0)
					diff_base_parent1 = repo.diff(base_version, parent1, context_lines=0)
					diff_base_parent2 = repo.diff(base_version, parent2, context_lines=0)

					merge_actions = get_actions(diff_base_final)
					parent1_actions = get_actions(diff_base_parent1)
					parent2_actions = get_actions(diff_base_parent2)

					commits_metrics[commit.hex] = calculate_metrics(merge_actions, parent1_actions, parent2_actions, detailed)
				else:
					print(commit.hex + " - this merge doesn't have a base version")
	except:
		print ("Unexpected error")
		print (traceback.format_exc())

	return commits_metrics	

def delete_repo_folder(folder):
		shutil.rmtree(folder)

def calculate_metrics(merge_actions, parent1_actions, parent2_actions, detailed):	
	metrics = {}

	parents_actions = set(parent1_actions).union(parent2_actions)

	additional_metric = calculate_additional_effort(merge_actions, parents_actions)
	metrics['merge effort'] = additional_metric/len(merge_actions)

	if(detailed):
		metrics['branch1'] = len(parent1_actions)
		metrics['branch2'] = len(parent2_actions)
		metrics['merge'] = len(merge_actions)

		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions, parents_actions)
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)
		metrics['additional'] = additional_metric


	return metrics

			
def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--url", help="set an url for a git repository")
	group.add_argument("--local", help="set the path of a local git repository")
	parser.add_argument("--commit", nargs='+', help="set the commit (or a list of commits separated by comma) to analyse. Default: all merge commits")
	parser.add_argument("--detailed",action='store_true', help="show all metrics (size of branch1, branch2 and merge, branches rework, wasted actions and additional actions")
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

	commits_metrics = analyse(commits, repo, args.detailed)
	print(commits_metrics)

	if args.url:
		delete_repo_folder(repo.workdir)

	print(datetime.now() - startTime)

	
if __name__ == '__main__':
	main()	

