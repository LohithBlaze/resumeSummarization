import tika
import spacy
import os
from tika import parser
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def calculateRanking(resumeData):
        score = 0
        # print(resumeData)
        for entity in resumeData:
                if fuzz.ratio(entity, "Name") > 70 or fuzz.ratio(entity, "Companies worked at") > 70:
                        continue
                if fuzz.ratio(entity, "Degree") > 70:
                        temp = resumeData[entity]
                        if isinstance(temp, list):
                                temp = ' '.join(temp)
                        choicesBE = ["btech", "bachelor", "bca", "be"]
                        choicesMSorPhd = ["masters", "Mtech", "MS", "mca", "phd"]

                        results1 = process.extract(temp, choicesBE)
                        results2 = process.extract(temp, choicesMSorPhd)
                        for result in results1:
                                if result[1] > 50:
                                        score += 1
                                        break
                        for result in results2:
                                if result[1] > 50:
                                        score += 1
                if fuzz.ratio(entity, "experience") > 50:
                        temp = resumeData[entity]
                        if isinstance(temp, list):
                                temp = ' '.join(temp)
                        experience = 0
                        for i in temp.split():
                                try:
                                        experience = float(i)
                                        break
                                except Exception as e:
                                        pass
                        if experience > 3:
                                score += 1

                if fuzz.ratio(entity, "skills") > 50:
                        skills = ["go lang", "nodejs", "nlp", "machine learning", "computer vision", "natural language processing"]
                        
                        temp = resumeData[entity]
                        if isinstance(temp, list):
                                temp = ' '.join(temp)
                        results3 = process.extract(temp, skills)
                        for result in results3:
                                if result[1] > 50:
                                        score += 1
        
        return score

print(sys.argv[1])
parsed = parser.from_file(sys.argv[1])

print("loading the model")
nlp2 = spacy.load(os.getcwd())
doc = nlp2(parsed['content'])




f=open("resume"+".txt","w")
d={}

for ent in doc.ents:
    d[ent.label_]=[]
for ent in doc.ents:
    d[ent.label_].append(ent.text)

for i in set(d.keys()):

    f.write("\n\n")
    f.write(i +":"+"\n")
    for j in set(d[i]):
        f.write(j.replace('\n','')+"\n")

score = calculateRanking(d)

# print(score)

f.write("Rating")
f.write("\n")
f.write(str(score))
f.close()
