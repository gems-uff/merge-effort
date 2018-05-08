from pygit2 import *
import os
import sys
import shutil


class Action(object):
	def __init__(self, content, file_name, action, new_line, old_line):
		self.content = content
		self.file_name = file_name
		self.action = action
		self.new_line = new_line
		self.old_line = old_line


def print_actions(list_actions):
	for a in list_actions:
		print("-------------------------------------------------------------------- \nPrinting Line:")
		print ("File: " + a.file_name)
		print ("Content: " + a.content)
		print ("New line: " +str(a.new_line))
		print ("Old line: " +str(a.old_line))
		print ("File action: " + a.action)
		print("-------------------------------------------------------------------- \n")


def actions_to_set(list_actions):
	set_actions = set()

	for action in list_actions:
		aux = (action.file_name, action.content, action.action)

		set_actions.add(aux)

	return set_actions


def set_actions(diff_a_b):
	list_actions = []
	
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		
		for h in d.hunks:
			
			for l in h.lines:
				action = Action(l.content, file_name, l.origin, l.new_lineno, l.old_lineno)
				list_actions.append(action)

	return list_actions

def calculate_metrics(commits):
	commits_metrics = {}
	for commit in commits:

		if (len(commit.parents)==2):
			parent1 = commit.parents[0]
			parent2 = commit.parents[1]

			base = repo.merge_base(parent1.hex, parent2.hex)
			base_version = repo.get(base)
			
			diff_base_final = repo.diff(base_version, commit)
			diff_base_parent1 = repo.diff(base_version, parent1)
			diff_base_parent2 = repo.diff(base_version, parent2)


			merge_actions = set_actions(diff_base_final)
			parent1_actions = set_actions(diff_base_parent1)
			parent2_actions = set_actions(diff_base_parent2)
			
			merge_actions_set = actions_to_set(merge_actions)
			parent1_actions_set = actions_to_set(parent1_actions)
			parent2_actions_set = actions_to_set(parent2_actions)

			metrics = {}

			parents_actions_set = set(parent1_actions_set).union(parent2_actions_set)

			rework_actions = set(parent1_actions_set).intersection(parent2_actions_set)
			rework_actions_relative = '{:.0%}'.format(len(rework_actions) / len(parents_actions_set))
			rework_actions_absolute = len(rework_actions)

			metrics['Parents rework - relative'] = rework_actions_relative
			metrics['Parents rework - absolute'] = rework_actions_absolute


			wasted_actions = parents_actions_set - merge_actions_set
			wasted_actions_relative = '{:.0%}'.format(len(wasted_actions) / len(parents_actions_set))
			wasted_actions_absolute = len(wasted_actions)

			metrics['Wasted actions - relative'] = wasted_actions_relative
			metrics['Wasted actions - absolute'] = wasted_actions_absolute


			additional_actions = merge_actions_set - parents_actions_set
			additional_actions_relative = '{:.0%}'.format(len(additional_actions) / len(merge_actions_set))
			additional_actions_absolute = len(additional_actions)

			metrics['Additional actions - relative'] = additional_actions_relative
			metrics['Additional actions - absolute'] = additional_actions_absolute


			no_effort = merge_actions_set.intersection(parents_actions_set)
			no_effort_relative = '{:.0%}'.format(len(no_effort) / len(merge_actions_set))
			no_effort_absolute = len(no_effort)


			metrics['No effort actions - relative'] = no_effort_relative
			metrics['No effort actions - absolute'] = no_effort_absolute


			commits_metrics[commit.hex] = metrics

	return commits_metrics	



#repo_url = 'git://github.com/tayanemoura/teste_merge.git'

repo_url = sys.argv[1]

current_working_directory = os.getcwd()

repo_path = current_working_directory + "/" + sys.argv[2]

repo = clone_repository(repo_url, repo_path) 

commits_metrics = calculate_metrics(repo.walk(repo.head.target, GIT_SORT_TIME | GIT_SORT_REVERSE))

print(commits_metrics)

shutil.rmtree(repo_path)
		

