from nltk.corpus import stopwords


def word_getter(s):
    s = s.lower()
    word_list = s.split()
    filtered_words = set([word for word in word_list if word not in stopwords.words('english')])
    return filtered_words

def is_similar(s1, s2, cutoff=0.125):
    a = word_getter(s1)
    b = word_getter(s2)
    jaccard = len(a.intersection(b)) / len(a.union(b))
    return (jaccard > cutoff)

def get_unique(sites):
    unique = set()
    for ls in sites:
        for art1 in ls:
            is_unique = True
            for art2 in unique:
                if is_similar(art1[1], art2[1]):
                    is_unique = False
            if is_unique:
                unique.add(art1)

    return unique
