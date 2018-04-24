from pygit2 import *
import os
import sys


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
	#set_actions = {}
	set_actions = set()

	for action in list_actions:
		aux = (action.file_name, action.content, action.action)

		set_actions.add(aux)

	print (set_actions)
	return set_actions


def set_actions(diff_a_b):
	list_actions = []
	diff_a_b.find_similar()
	for d in diff_a_b:
		#here gets the similiarity percentage
		
		#print (d.delta.similarity)
		if d.delta.similarity == 100:
			#print(d.delta.new_file.path)
			#print(d.delta.old_file.path)
			action = Action(d.delta.old_file.path, d.delta.new_file.path, "renamed_file", -2, -2)
			list_actions.append(action)

		else:
			#print (d.patch)
			file_name = d.delta.new_file.path
			for h in d.hunks:
				#print (h)
				#print (h.header)
				for l in h.lines:
					action = Action(l.content, file_name, l.origin, l.new_lineno, l.old_lineno)
					list_actions.append(action)

	return list_actions


#orig_stdout = sys.stdout
#f = open('out.txt', 'w')
#sys.stdout = f

#repo_url = 'git://github.com/tayanemoura/teste_merge.git'

repo_url = sys.argv[1]

current_working_directory = os.getcwd()

repo_path = current_working_directory + "/" + sys.argv[2]


repo = clone_repository(repo_url, repo_path) #

for commit in repo.walk(repo.head.target, GIT_SORT_TIME | GIT_SORT_REVERSE):
	
	if (len(commit.parents)==2):
		print("-------------------------------------------------------------------- \nCommit:")
		print (commit.hex)
		print("-------------------------------------------------------------------- \nParents:")
		parent1 = commit.parents[0]
		parent2 = commit.parents[1]

		print (parent1.hex)
		print (parent2.hex)


		base = repo.merge_base(parent1.hex, parent2.hex)
		print("-------------------------------------------------------------------- \nMerge base:")
		print(base)


		base_version = repo.get(base)
		
		diff_base_final = repo.diff(base_version, commit)
		diff_base_parent1 = repo.diff(base_version, parent1)
		diff_base_parent2 = repo.diff(base_version, parent2)


		merge_actions = set_actions(diff_base_final)
		parent1_actions = set_actions(diff_base_parent1)
		parent2_actions = set_actions(diff_base_parent2)
		

		print ("\nmerge actions")
		merge_actions_set = actions_to_set(merge_actions)
		print ("parent 1 actions")
		parent1_actions_set = actions_to_set(parent1_actions)
		print ("parent 2 actions")
		parent2_actions_set = actions_to_set(parent2_actions)
		print()


		parents_actions_set = set(parent1_actions_set).union(parent2_actions_set)

		rework_actions = set(parent1_actions_set).intersection(parent2_actions_set)
		#print ("\nrework actions")
		#print (rework_actions)
		#print('Rework actions: {:.0%}'.format(len(rework_actions) / len(parents_actions_set)))


		print("--------------------------------------------------------------------\nWasted Effort\n")
		wasted_actions = parents_actions_set - merge_actions_set
		print (wasted_actions)
		print('Wasted effort: {:.0%}'.format(len(wasted_actions) / len(parents_actions_set)))

		additional_actions = merge_actions_set - parents_actions_set
		print("--------------------------------------------------------------------\nAdditional Effort\n")
		print('Additional effort: 	{:.0%}'.format(len(additional_actions) / len(merge_actions_set)))
		print (additional_actions)
		
		no_effort = merge_actions_set.intersection(parents_actions_set)
		print("--------------------------------------------------------------------\n No Effort\n")
		print(no_effort)


		print("-------------------------------------------------------------------- \nEnd - Commit \n")
			



#sys.stdout = orig_stdout
#f.close()			

