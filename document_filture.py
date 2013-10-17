import docclass

c1 =  docclass.naivebayes(docclass.getWords)

docclass.sampletrain(c1)
print c1.prob('quick rabbit', 'good')

print c1.classIfy('quick money')
