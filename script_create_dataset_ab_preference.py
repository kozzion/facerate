import os

import face_recognition
import numpy as np

from persistency import Persistency

ps = Persistency('C:/DataSets/SCUTFBP5500')

# constants
sample_count = 5000

# functions
def create_preference_list(ratingDict, sampleCount):
    imageNameList = list(ratingDict.keys())
    preferceList = []
    for i in range(sampleCount):
        sample = np.random.choice(len(ratingDict), 2)
        image_name_a = imageNameList[sample[0]]
        image_name_b = imageNameList[sample[1]]
        rating_a = ratingDict[image_name_a]
        rating_b = ratingDict[image_name_b]
        if rating_b < rating_a:
            preferceList.append((image_name_a, image_name_b, True))
        else:
            preferceList.append((image_name_a, image_name_b, False))
    return preferceList



#load dataset
item_dict = {}
rating_list = ps.load_rating_list()
rating_dict_dict = {}
for rating in rating_list:
    rater = rating[0]
    if not rater in rating_dict_dict:
        rating_dict_dict[rater] = {}

for rating in rating_list:
    rater = rating[0]
    item_name = os.path.splitext(rating[1])[0]
    item_dict[item_name] = True
    rating_dict_dict[rater][item_name] = float(rating[2])


preferce_list = []
for rater in rating_dict_dict:
    preferce_list.extend(create_preference_list(rating_dict_dict[rater], sample_count))

print(len(preferce_list))
item_list = list(item_dict.keys())
ps.save_dataset('preferce_list_all', (item_list, preferce_list))
