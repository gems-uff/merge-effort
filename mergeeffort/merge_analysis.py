from datetime import datetime
startTime = datetime.now()
from collections import Counter

from pygit2 import *
import os
import shutil
import argparse
import time
import traceback


def get_actions(diff_a_b):
	actions = Counter()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				actions.update([file_name+l.origin+l.content])
	return actions

def clone(url):
	repo_url = url
	current_working_directory = os.getcwd()
	repo_path = current_working_directory + "/build/" + str(time.time())
	repo = clone_repository(repo_url, repo_path) 

	return repo


def calculate_rework(parent1_actions, parent2_actions):
	rework_actions = parent1_actions & parent2_actions
	return (sum(rework_actions.values()))

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions
	return (sum(wasted_actions.values()))

def calculate_additional_effort(parents_actions, merge_actions):
	additional_actions = merge_actions - parents_actions
	return (sum(additional_actions.values()))


def analyse(commits, repo, normalized=False):
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

					commits_metrics[commit.hex] = calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized)
				else:
					print(commit.hex + " - this merge doesn't have a base version")
	except:
		print ("Unexpected error")
		print (traceback.format_exc())

	return commits_metrics	

def delete_repo_folder(folder):
		shutil.rmtree(folder)

def calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized):	
	metrics = {}

	parents_actions = parent1_actions + parent2_actions 

	if(normalized):
		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)/sum(parents_actions.values())
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)/sum(parents_actions.values())
		metrics['merge_effort'] =calculate_additional_effort(parents_actions, merge_actions)/sum(merge_actions.values())

	else:
		metrics['branch1'] = len(parent1_actions)
		metrics['branch2'] = len(parent2_actions)
		metrics['merge'] = len(merge_actions)
		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)
		metrics['merge_effort'] = calculate_additional_effort(parents_actions, merge_actions)
		
	return metrics

			
def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--url", help="set an url for a git repository")
	group.add_argument("--local", help="set the path of a local git repository")
	parser.add_argument("--commit", nargs='+', help="set the commit (or a list of commits separated by comma) to analyse. Default: all merge commits")
	parser.add_argument("--normalized",action='store_true', help="show all metrics (size of branch1, branch2 and merge, branches rework, wasted actions and additional actions")
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

	commits_metrics = analyse(commits, repo, args.normalized)
	print(commits_metrics)
	print("Total of merge commits: " + str(len(commits_metrics)))
	if args.url:
		delete_repo_folder(repo.workdir)

	print(datetime.now() - startTime)

	
if __name__ == '__main__':
	main()	

