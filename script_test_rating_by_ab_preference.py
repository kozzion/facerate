import sys
sys.path.append('./ranking/')
import os
import random
import tools_ranking
import face_recognition
import numpy as np

from persistency import Persistency

ps = Persistency('C:/DataSets/SCUTFBP5500')


#load dataset
item_name_list, item_preference_ab_list = ps.load_dataset('preferce_list_all')
ranking_dict_a = tools_ranking.generate_ranking_dict_random(item_name_list, item_preference_ab_list)
random.shuffle(item_preference_ab_list)
ranking_dict_b = tools_ranking.generate_ranking_dict_random(item_name_list, item_preference_ab_list)
random.shuffle(item_preference_ab_list)

ranking_dict_c = tools_ranking.generate_ranking_dict_elo(item_name_list, item_preference_ab_list)
random.shuffle(item_preference_ab_list)
ranking_dict_d = tools_ranking.generate_ranking_dict_elo(item_name_list, item_preference_ab_list)

mrd = tools_ranking.compute_mean_rank_difference(ranking_dict_a, ranking_dict_a)
print(mrd)
mrd = tools_ranking.compute_mean_rank_difference(ranking_dict_a, ranking_dict_b)
print(mrd)
mrd = tools_ranking.compute_mean_rank_difference(ranking_dict_a, ranking_dict_c)
print(mrd)
mrd = tools_ranking.compute_mean_rank_difference(ranking_dict_c, ranking_dict_d)
print(mrd)
