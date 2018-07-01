import pytest 
import pygit2
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mergeeffort.merge_analysis as merge_analysis
from collections import Counter

def test_wasted_effort():
	parents_actions = Counter({'main.py+print("D")\n': 2, 'main.py-print("C")\n': 1, 'main.py+print("Good Bye")\n': 1, 'main.py+print("End")\n': 1, 'main.py+print("F")\n': 1, 'main.py+print("Z")\n': 1})
	merge_actions = Counter({'main.py-A = "Hello"\n': 1, 'main.py-print(A)\n': 1, 'main.py-B = "World"\n': 1, 'main.py-print(B)\n': 1, 'main.py-print("C")\n': 1, 'main.py+import string\n': 1, 'main.py+\n': 1, 'main.py+print("Hello World")\n': 1, 'main.py+for c in string.ascii_lowercase:\n': 1, 'main.py+\tprint(c)\n': 1, 'main.py+print("Good Bye")\n': 1})
	assert(merge_analysis.calculate_wasted_effort(parents_actions, merge_actions) == 5)

def test_rework():
	parent1_actions = Counter({'main.py-print("C")\n': 1, 'main.py+print("D")\n': 1, 'main.py+print("Good Bye")\n': 1, 'main.py+print("End")\n': 1})
	parent2_actions = Counter({'main.py+print("D")\n': 1, 'main.py+print("F")\n': 1, 'main.py+print("Z")\n': 1})
	assert(merge_analysis.calculate_rework(parent1_actions, parent2_actions) == 1)

def test_additional():
	parents_actions = Counter({'main.py+print("D")\n': 2, 'main.py-print("C")\n': 1, 'main.py+print("Good Bye")\n': 1, 'main.py+print("End")\n': 1, 'main.py+print("F")\n': 1, 'main.py+print("Z")\n': 1})
	merge_actions = Counter({'main.py-A = "Hello"\n': 1, 'main.py-print(A)\n': 1, 'main.py-B = "World"\n': 1, 'main.py-print(B)\n': 1, 'main.py-print("C")\n': 1, 'main.py+import string\n': 1, 'main.py+\n': 1, 'main.py+print("Hello World")\n': 1, 'main.py+for c in string.ascii_lowercase:\n': 1, 'main.py+\tprint(c)\n': 1, 'main.py+print("Good Bye")\n': 1})
	assert(merge_analysis.calculate_additional_effort(parents_actions, merge_actions) == 9)


def test_metrics():
	repo = merge_analysis.clone("https://github.com/tayanemoura/teste_merge_2.git")
	commits = [repo.get("6438a3fd88c250aab1e523e5017ba2b147fe9fe7")]
	assert(merge_analysis.analyse(commits, repo) == {'6438a3fd88c250aab1e523e5017ba2b147fe9fe7': {'branch1': 4, 'branch2': 3, 'merge': 11, 'rework': 1, 'wasted': 5, 'merge_effort': 9}})
	merge_analysis.delete_repo_folder(repo.workdir)
