gdb --args main gibbs ap/ap.short settings.txt outdir
run
python tree.py txt /home/genevieve/mit-whoi/hlda/outdir/run003/mode ap/vocab.txt ap/ap.dat out_tree

./main gibbs generative/sim.dat settings.txt simout 
python tree.py txt /home/genevieve/mit-whoi/hlda/simout/run006/mode generative/sim_vocab.txt generative/sim.dat simtree_out
