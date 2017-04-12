import tree

docmap = tree.read_jacm_docmap("/home/genevieve/mit-whoi/hlda/ap/ap.dat")
state = tree.read_state("GOO/mode", vocab, 5)
tree.add_assignments_to_tree('GOO/mode.assign', state['tree'])
tree.write_topic_tree_ascii(state, docmap, 'GOO.txt')
tree.write_topic_tree_dot(goo, "Good.dot", 0, 0)
