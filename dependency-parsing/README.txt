1.
b) Description of projection dependency algorithm

For all the nodes in the dependency graph,
	if nodes are head nodes, capture the set of child-parent relationship in an arc_list
For each parent-child relationship in the arc_list set, 
	ensure that the location of child < parent
	if there is an arc between child and parent node
	if it is from a node that is outside child and parent
		then it is non- projective 		
	else it is projective.

--------------------------------------------------------------------------------------------------------------

c) 
Projective dependency graph sentence:
I shot an elephant yesterday.

Non- projective dependency graph sentence:
John saw a dog which was a Siberian Husky.
 

==============================================================================================================>
2.

b) Bad features model performance

UAS: 0.23023302131
LAS: 0.125273849831

===============================================================================================================>
3.

***English.model is generated using dev corpus. ***

a)

Features Implemetation					Complexity		Performance

                Base								O(n)			Swedish
                        											UAS: 0.357498506274
                        											LAS: 0.238996215893
                        									
                        											English
                        											UAS: 0.397530864198
                        											LAS: 0.328395061728
                        									
                        											Danish
                        											UAS: 0.72754491018
                        											LAS: 0.647704590818
		
Checking If length of stack > 0,
if length of buffer >0	
Checking for and adding lemma 
to the first element of the 
stack and buffer respectively					O(n)		Swedish
                        											UAS: 0.367855008962
                        											LAS: 0.249950209122
                        											
                        											English
                        											UAS: 0.4
                        											LAS: 0.338271604938
                        											 
                        											Danish
                        											UAS: 0.744111776447
                        											LAS: 0.667265469062
Checking for and adding Tag
to the first element of the 
stack and buffer respectively					O(n)		Swedish
                        											UAS: 0.74706233818
                        											LAS: 0.645488946425
                        											
                        											English
                        											UAS: 0.575308641975
                        											LAS: 0.545679012346
                        											 
                        											Danish
                        											UAS: 0.763073852295
                        											LAS: 0.688023952096
Checking for and adding ctag 
to the first element of the 
stack and buffer respectively					O(n)		Swedish
                        											UAS: 0.74526986656
                        											LAS: 0.646883091018
                        											
                        											English
                        											UAS: 0.577777777778
                        											LAS: 0.553086419753
                        											 
                        											Danish
                        											UAS: 0.761477045908
                        											LAS: 0.688622754491
If length of stack > 1
Checking for and adding tag 
to the second element of 
the stack							                O(n)		Swedish
                        											UAS: 0.744274048994
                        											LAS: 0.644094801832
                        
                        											English
                        											UAS: 0.587654320988
                        											LAS: 0.558024691358
                        
                        											Danish
                        											UAS: 0.759680638723
                        											LAS: 0.686027944112

Checking if length of buffer >1	
Checking for and adding word 
and tag to the second element 
of the buffer							            O(n)		Swedish
                        											UAS: 0.79008165704
                        											LAS: 0.682732523402
                        											 
                        											English
                        											UAS: 0.743209876543
                        											LAS: 0.708641975309
                        											
                        											Danish
                        											UAS: 0.80119760479
                        											LAS: 0.72095808383

-----------------------------------------------------------------------------------------------------------------------------------------										
d)
The complexity of the Arc-Eager-Shift-Reduce parser is O(n). 
But the trade off is that it only works for projective sentences and doesn't account for non projective sentences.
A possible way to address this could be- to use a post processor to a projective dependency parsing algorithm to identify and resolve 
non-projectivity (or) to add extra transitions that can at least model most non-projective structures.
