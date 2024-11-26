FinalProj:
	echo "#!/bin/bash" > FinalProj
	echo "python main.py \"\$$@\"" >> FinalProj
	chmod u+x FinalProj
	
clean:
	rm -f FinalProj