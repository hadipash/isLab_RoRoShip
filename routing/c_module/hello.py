import graph_m#helloworld	# C module
import numpy
'''
a = numpy.array([[1,2,3],
                  [4,5,6],
                  [7,8,9],
                  [3,5,0]])
b = helloworld.mean(a)
print b[2][2]
c = helloworld.update(a)
print c
'''
b=[[1 for y in range(50)]for x in range(50)]
a = numpy.array(b)
print graph_m.init(2,4,3,a)
print graph_m.path_chk(30,4,32,8,2,4,3,a);

#a = numpy.array([[1,2,3,4,5]], dtype="int")
#b = numpy.array([[[1,2,3,4,5]]], dtype="int")
#print helloworld.func(a,b)

