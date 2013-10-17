#coding:utf-8
import jieba
import random
import re
import math


def getWords(doc):
    words = []
    tmp = jieba.cut(doc)
    for word in tmp:
        if word not in words:
            words.append(word)
    return words

def sampletrain(c1):
    c1.train('Nobody owns the water.', 'good')
    c1.train('the quick rabbit jumps fences', 'good')
    c1.train('buy pharmaceuticals now', 'bad')
    c1.train('make quick money at the online casino', 'bad')
    c1.train('the quick brown fox jumps', 'good')

class classIfier(object):
    def __init__(self, getFeatures, fileName = None):
        self.fc = {}
        self.cc = {}
        self.thresholds = {}
        self.getFeatures = getFeatures

    def infc(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1
    def incc(self, cat):
        self.cc.setdefault(cat, 0);
        self.cc[cat] += 1
    def fCount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    def catCount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0
    def totalCount(self):
        return float(sum(self.cc.values()))
    def categories(self):
        return self.cc.keys()

    def fProb(self, f, cat):    
        if self.catCount(cat) == 0:
            return 0.0
        return self.fCount(f, cat) / self.catCount(cat)

    def weightDprob(self, f, cat, prf, weight = 1.0, ap = 0.5):  
        basicProb = prf(f, cat)
        totals = sum([self.fCount(f, c) for c in self.categories()])

        bp = ((weight * ap) + (totals * basicProb)) / (weight + totals)
        
        return bp

    def train(self, item, cat):
        features = self.getFeatures(item)

        for f in features:
            self.infc(f, cat)
        self.incc(cat)

    def setThreshold(self, cat, t):
        self.thresholds[cat] = t
    def getThreshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

class naivebayes(classIfier):
    def docprob(self, item, cat):
        features = self.getFeatures(item)
        p = 1
        for  f in features:
            p *= (self.weightDprob(f, cat, self.fProb))
        return p

    def prob(self, item, cat):
        catProb = self.catCount(cat) / self.totalCount()
        docProb = self.docprob(item, cat)
        print catProb
        print docProb
        return docProb * catProb
    def classIfy(self, item, defaultCat = 'unknow'):
        probs = {}
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max - probs[cat]
                best = cat
        for cat in probs:
            if cat == best: continue
            if probs[cat] * self.getThreshold(best) > probs[best]:
                return defaultCat
        return best


        






