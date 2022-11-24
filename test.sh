# !bin/bash

psql \
	    -X \
	    -U postgres \
	    password=postgres
        
create DATABASE testSSH;