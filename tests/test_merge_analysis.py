import pytest 
import pygit2
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mergeeffort.merge_analysis as merge_analysis

def test_wasted_effort():
	parents_actions = {('main.py', 'print("End")\n', '+'), ('main.py', 'print("D")\n', '+'), ('main.py', 'print("Good Bye")\n', '+'), ('main.py', 'print("C")\n', '-'), ('main.py', 'print("Z")\n', '+'), ('main.py', 'print("F")\n', '+')}
	merge_actions = {('main.py', '\n', '+'), ('main.py', 'A = "Hello"\n', '-'), ('main.py', 'for c in string.ascii_lowercase:\n', '+'), ('main.py', 'B = "World"\n', '-'), ('main.py', '\tprint(c)\n', '+'), ('main.py', 'print(B)\n', '-'), ('main.py', 'print("Good Bye")\n', '+'), ('main.py', 'import string\n', '+'), ('main.py', 'print("Hello World")\n', '+'), ('main.py', 'print(A)\n', '-'), ('main.py', 'print("C")\n', '-')}
	assert(merge_analysis.calculate_wasted_effort(parents_actions, merge_actions) == 4)

def test_rework():
	parent1_actions ={('main.py', 'print("End")\n', '+'), ('main.py', 'print("Good Bye")\n', '+'), ('main.py', 'print("C")\n', '-'), ('main.py', 'print("D")\n', '+')}
	parent2_actions = {('main.py', 'print("Z")\n', '+'), ('main.py', 'print("F")\n', '+'), ('main.py', 'print("D")\n', '+')}
	parents_actions = set(parent1_actions).union(parent2_actions)
	assert(merge_analysis.calculate_rework(parent1_actions, parent2_actions, parents_actions) == 1)

def test_additional():
	parents_actions = {('main.py', 'print("End")\n', '+'), ('main.py', 'print("D")\n', '+'), ('main.py', 'print("Good Bye")\n', '+'), ('main.py', 'print("C")\n', '-'), ('main.py', 'print("Z")\n', '+'), ('main.py', 'print("F")\n', '+')}
	merge_actions = {('main.py', '\n', '+'), ('main.py', 'A = "Hello"\n', '-'), ('main.py', 'for c in string.ascii_lowercase:\n', '+'), ('main.py', 'B = "World"\n', '-'), ('main.py', '\tprint(c)\n', '+'), ('main.py', 'print(B)\n', '-'), ('main.py', 'print("Good Bye")\n', '+'), ('main.py', 'import string\n', '+'), ('main.py', 'print("Hello World")\n', '+'), ('main.py', 'print(A)\n', '-'), ('main.py', 'print("C")\n', '-')}
	assert(merge_analysis.calculate_additional_effort(merge_actions, parents_actions) == 9)


def test_metrics():
	repo = merge_analysis.clone("https://github.com/tayanemoura/teste_merge_2.git")
	commits = [repo.get("6438a3fd88c250aab1e523e5017ba2b147fe9fe7")]
	assert(merge_analysis.analyse(commits, repo) == {'6438a3fd88c250aab1e523e5017ba2b147fe9fe7': {'branch1': 4, 'branch2': 3, 'merge': 11, 'Parents rework': 1, 'Wasted actions': 4, 'Additional actions': 9}})
	merge_analysis.delete_repo_folder(repo.workdir)
