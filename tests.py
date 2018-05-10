import pytest 
import merge_analysis
import pygit2


def test_no_effort():
	parents_actions = {('new_code.py', 'print ("Hello IC")\n', '+'), ('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Uff")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	merge_actions = {('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Everybody")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	
	assert(merge_analysis.calculate_no_effort(merge_actions, parents_actions) == ['67%', 2])

def test_wasted_effort():
	parents_actions = {('new_code.py', 'print ("Hello IC")\n', '+'), ('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Uff")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	merge_actions = {('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Everybody")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	assert(merge_analysis.calculate_wasted_effort(parents_actions, merge_actions) == ['50%', 2])

def test_rework():
	parent1_actions = {('new_code.py', 'print ("Hello World")', '-'), ('new_code.py', 'print ("Hello IC")\n', '+'), ('new_code.py', '\n\\ No newline at end of file\n', '>')}
	parent2_actions = {('new_code.py', 'print ("Hello World")', '-'), ('new_code.py', 'print ("Hello Uff")\n', '+'), ('new_code.py', '\n\\ No newline at end of file\n', '>')}
	parents_actions = set(parent1_actions).union(parent2_actions)
	assert(merge_analysis.calculate_rework(parent1_actions, parent2_actions, parents_actions) == ['50%', 2])

def test_additional():
	parents_actions = {('new_code.py', 'print ("Hello IC")\n', '+'), ('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Uff")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	merge_actions = {('new_code.py', '\n\\ No newline at end of file\n', '>'), ('new_code.py', 'print ("Hello Everybody")\n', '+'), ('new_code.py', 'print ("Hello World")', '-')}
	assert(merge_analysis.calculate_additional_effort(merge_actions, parents_actions) == ['33%', 1])


def test_metrics():
	repo = pygit2.Repository("/Users/tayanemoura/Documents/git/teste_merge")
	commits = [repo.get("175b655a2002891ba735ad53ee679b3718c6d997")]
	assert(merge_analysis.analyse(commits, repo) == {'175b655a2002891ba735ad53ee679b3718c6d997': {'Parents rework - relative': '50%', 'Parents rework - absolute': 2, 'Wasted actions - relative': '50%', 'Wasted actions - absolute': 2, 'Additional actions - relative': '33%', 'Additional actions - absolute': 1, 'No effort actions - relative': '67%', 'No effort actions - absolute': 2}})