library.scpt : library
	osacompile -o library.scpt library

clean:
	rm -f library.scpt *~
