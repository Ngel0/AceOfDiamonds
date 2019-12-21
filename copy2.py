#!E:/Programs/Anaconda3/envs/Project2/python

import os
import re
import pymorphy2
import sys
from gensim.models import Word2Vec

model = Word2Vec.load("E:/Desktop/PycharmProjects/Project2/mymodel.model")
model.init_sims(replace=True)

morph = pymorphy2.MorphAnalyzer()
punct = re.compile('^(.*?)([а-яА-ЯёЁ-]+)(.*?)$')
capit = re.compile('^[А-Я]+$')

pth_source = 'E:/Desktop/PycharmProjects/Project2/books_before/'
lst = os.listdir(pth_source)

pth_result = 'E:/Desktop/PycharmProjects/Project2/books_after/'

cotags = {'ADJF': 'ADJ',  # pymorphy2: word2vec
          'ADJS': 'ADJ',
          'ADVB': 'ADV',
          'COMP': 'ADV',
          'GRND': 'VERB',
          'INFN': 'VERB',
          'NOUN': 'NOUN',
          'PRED': 'ADV',
          'PRTF': 'ADJ',
          'PRTS': 'VERB',
          'VERB': 'VERB'}

capit_letters = [chr(x) for x in range(1040, 1072)] + ['Ё']


def search_neighbour(word, pos, gend='masc'):
    word = word.replace('ё', 'е')
    lex = word + '_' + cotags[pos]
    if lex in model:
        neighbs = model.most_similar([lex], topn=20)
        for nei in neighbs:
            lex_n, ps_n = nei[0].split('_')
            if '::' in lex_n:
                continue
            if cotags[pos] == ps_n:
                if pos == 'NOUN':
                    parse_result = morph.parse(lex_n)
                    for ana in parse_result:
                        if ana.normal_form == lex_n:
                            if ana.tag.gender == gend:
                                return lex_n
                elif cotags[pos] == 'VERB' and word[-2:] == 'ся':
                    if lex_n[-2:] == 'ся':
                        return lex_n
                elif cotags[pos] == 'VERB' and word[-2:] != 'ся':
                    if lex_n[-2:] != 'ся':
                        return lex_n
                else:
                    return lex_n
    return None


def flection(lex_neighb, tags):
    tags = str(tags)
    tags = re.sub(',[AGQSPMa-z-]+? ', ',', tags)
    tags = tags.replace("impf,", "")
    tags = re.sub('([A-Z]) (plur|masc|femn|neut|inan)', '\\1,\\2', tags)
    tags = tags.replace("Impe neut", "")
    tags = tags.split(',')
    tags_clean = []
    for t in tags:
        if t:
            if ' ' in t:
                t1, t2 = t.split(' ')
                t = t2
            tags_clean.append(t)
    tags = frozenset(tags_clean)
    prep_for_gen = morph.parse(lex_neighb)
    ana_array = []
    for ana in prep_for_gen:
        if ana.normal_form == lex_neighb:
            ana_array.append(ana)
    for ana in ana_array:
        try:
            flect = ana.inflect(tags)
        except:
            print(tags)
            return None
        if flect:
            word_to_replace = flect.word
            return word_to_replace
    return None


cash_neighb = {}

for fl in lst:
    if not fl.endswith('.txt'):
        continue
    print(fl)
    i = 0
    f = open(pth_source + fl, 'r', encoding='utf-8')
    fw = open(pth_result + '3.0_' + fl, 'w', encoding='utf-8')
    fs = open(pth_result + '3.0_Sample' + fl, 'w', encoding='utf-8')
    for line in f:
        new_line = []
        i += 1
        line = line.strip()
        words = line.split(' ')
        for word in words:
            struct = punct.findall(word)
            if struct:
                struct = struct[0]
            else:
                new_line.append(word)
                continue
            # print (struct)
            wordform = struct[1]
            if wordform:
                if capit.search(wordform):
                    new_line.append(word)
                    continue
                else:
                    if wordform[0] in capit_letters:
                        capit_flag = 1
                    else:
                        capit_flag = 0
                parse_result = morph.parse(wordform)[0]
                if 'Name' in parse_result.tag or 'Patr' in parse_result.tag:
                    new_line.append(word)
                    continue
                if parse_result.normal_form == 'глава':
                    new_line.append(word)
                    continue
                pos_flag = 0
                for tg in cotags:
                    if tg in parse_result.tag:
                        pos_flag = 1
                        lex = parse_result.normal_form
                        pos_tag = parse_result.tag.POS
                        if (lex, pos_tag) in cash_neighb:
                            lex_neighb = cash_neighb[(lex, pos_tag)]
                        else:
                            if pos_tag == 'NOUN':
                                gen_tag = parse_result.tag.gender
                                lex_neighb = search_neighbour(lex, pos_tag, gend=gen_tag)
                            else:
                                lex_neighb = search_neighbour(lex, pos_tag)
                            cash_neighb[(lex, pos_tag)] = lex_neighb
                        if not lex_neighb:
                            new_line.append(word)
                            break
                        else:
                            if pos_tag == 'NOUN':
                                if parse_result.tag.case == 'nomn' and parse_result.tag.number == 'sing':
                                    if capit_flag == 1:
                                        lex_neighb = lex_neighb.capitalize()
                                    new_line.append(struct[0] + lex_neighb + struct[2])
                                else:
                                    word_to_replace = flection(lex_neighb, parse_result.tag)
                                    if word_to_replace:
                                        if capit_flag == 1:
                                            word_to_replace = word_to_replace.capitalize()
                                        new_line.append(struct[0] + word_to_replace + struct[2])
                                    else:
                                        new_line.append(word)

                            elif pos_tag == 'ADJF':
                                if parse_result.tag.case == 'nomn' and parse_result.tag.number == 'sing':
                                    if capit_flag == 1:
                                        lex_neighb = lex_neighb.capitalize()
                                    new_line.append(struct[0] + lex_neighb + struct[2])
                                else:
                                    word_to_replace = flection(lex_neighb, parse_result.tag)
                                    if word_to_replace:
                                        if capit_flag == 1:
                                            word_to_replace = word_to_replace.capitalize()
                                        new_line.append(struct[0] + word_to_replace + struct[2])
                                    else:
                                        new_line.append(word)

                            elif pos_tag == 'INFN':
                                if capit_flag == 1:
                                    lex_neighb = lex_neighb.capitalize()
                                new_line.append(struct[0] + lex_neighb + struct[2])

                            elif pos_tag in ['ADVB', 'COMP', 'PRED']:
                                if capit_flag == 1:
                                    lex_neighb = lex_neighb.capitalize()
                                new_line.append(struct[0] + lex_neighb + struct[2])

                            else:
                                word_to_replace = flection(lex_neighb, parse_result.tag)
                                if word_to_replace:
                                    if capit_flag == 1:
                                        word_to_replace = word_to_replace.capitalize()
                                    new_line.append(struct[0] + word_to_replace + struct[2])
                                else:
                                    new_line.append(word)
                        break
                if pos_flag == 0:
                    new_line.append(word)
            else:
                new_line.append(''.join(struct))
        line_replace = ' '.join(new_line)
        if i < 21:
            fs.write(line_replace + '\n')
        fw.write(line_replace + '\n')
    f.close()
    fw.close()
    fs.close()





