# layout_optimisation
Work done on the Raman Project at Sacha Engineering:

Summer-2023 attempt:
Some greedy heuristics have been tried. This shall be published as the v1.0 of the program.
It does well for small number of squares, upto 25 or so.
Remaining issues to be solved:
1. Writing a program for populating the required data structures which adapts to the problem at hand suitably.
2. Dealing with the case where multiple branches of lengths more than one meet at a particular master.
Disclaimer:
The usage of words "master" and "slave" is a common indicative chosen by our team. It by no means supports any
form of "slavery".

Winter-2023 attempt:
Several methods were tried. Initial results using the IPOPT solver proved to be extremely encouraging.
But, the fact that it converges to a local point of infeasibility was troublesome in some cases. Also, it worked well
with shapes which lack orientation, like a circle. It is good in terms of scaling and running times though. We would
explore other methods in the meantime.
This concludes v2.0 of the code. Although a lot of work remains to be done.

Summer-2024 attempt:
This marks the final stage of the code. We have achieved the desired results. It is quite scalable. It works even for
500 rectangles. It considers both the orientations of the rectangles. It satifies all constraints, with a certain 
threshold. The modelling of this problem as a CSP (Constraint-Satisfaction Problem) is very useful and fast.
Additionally, area optimisations were also made. 
All the tested cases went through smoothly, with a running time of less than 5 minutes!
This is being pubslished as v3.0, and the final version of the code, as the desired problem is absolutely solved
and put to bed!
