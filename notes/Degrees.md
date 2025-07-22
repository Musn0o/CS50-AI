#### Step 1

To find the shortest path we have to identify use the BFS because it's faster than DFS. We will have to declare a **Starting point (Initial State)** of course without any actions or parent because there is nothing before this point, after that we have to assign this Starting point to the frontier which will use it for navigation. The frontier is gonna be QueueFrontier because we are using BFS just like we agreed.

This is a snippet for the initialize:

```python
# Initialize frontier to just the starting position
start_node = Node(state=source, parent=None, action=None)
frontier = QueueFrontier()
frontier.add(start_node)
```

#### Step 2

After that we have to initialize empty set to track our explored nodes by the frontier to avoid revisiting them. And start exploring in a while loop with a check for empty state if it's empty then return none because nothing left to explore and we didn't get a path. Now declare a node variable and assign it by using the frontier's remove function, if the node state is the target return the reversed path to this node by using a while loop that follows the node's parent if it's not None and append the node's action and state (a, s) and assigning the node to it's parent to check the next parent until we reach None the loop ends and have the reversed path. Finally If our node passed the first 2 checks then it's time to add it to the explored set to avoid revisiting it.

Here's a snippet for this part:

```python
# Initialize an empty explored set
explored = set()
# Searching for solution
while True:
	# If nothing left in frontier, no relation between the actors
	if frontier.empty():
		return None
		
	# Remove the first node from the frontier for exploration
	current_node = frontier.remove()
	
	# Checking if we got our target(actor)
	if current_node.state == target:
		path = []
		while current_node.parent is not None:
			path.append((current_node.action, current_node.state))
			current_node = current_node.parent
		path.reverse()
		return path

	# Mark target(actor) as explored
	explored.add(current_node.state)
```

#### Step 3

 Now start a loop for action and state in neighbors_for_person what's that? neighbors_for_person function takes param person_id which in our case the node.state then it returns (movie_id, person_id) pairs for people who starred with a given person. So we got a set of pairs and we are looping in it, but only if the state isn't already in the frontier and isn't in the explored set (this prevents adding duplicate nodes and revisiting explored nodes). Now we will redo the first step but this time for a child and with assigned values instead of a starting point without a parent we got a child, that has a different state, a parent and an action. We already got the action and the state from the neighbors, and the parent will be the current node, now add this child to the frontier for navigation.

```python
# Moving to the next node(target_actor)
for movie_id, actor_id in neighbors_for_person(current_node.state):
	if not frontier.contains_state(actor_id) and actor_id not in explored:
		new_node = Node(state=actor_id, parent=current_node, action=movie_id)
		frontier.add(new_node)
```