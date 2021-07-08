
from version2.models import *
import pickle

def setup():
    with open('algorithms.txt', 'r') as fr:
        algs = set([line.strip() for line in fr.readlines()])

    algs.add('NO_CHOICE')
    for alg in algs:
        Algorithm(name=alg).save()

    for _ in range(5):
        TopScore().save()

    with open('version2/snippet.pickle', 'rb') as fr:
        qsl = pickle.load(fr)
        for i, q in enumerate(qsl[:10]):
            Query(query_name=q.query, query_id=i+1, num_fake=2).save()
        for i, q in enumerate(qsl[10:]):
            Query(query_name=q.query, query_id=i+11, num_fake=2).save()

        