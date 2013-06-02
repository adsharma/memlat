simple.so: simple.o
	gcc -shared simple.o -o simple.so

clean:
	$(RM) *.o *.so
