import random
import operator

# distance measure
def compute_mean_rank_difference(ranking_dict_a, ranking_dict_b):
    rank_difference_sum = 0
    for item_name in ranking_dict_a:
        ranking_a = ranking_dict_a[item_name]
        ranking_b = ranking_dict_b[item_name]
        rank_difference_sum = rank_difference_sum + abs(ranking_a - ranking_b)
    return 3 * rank_difference_sum / (len(ranking_dict_a) * len(ranking_dict_a))

# random ranks
def generate_ranking_dict_random(item_name_list, item_preference_ab_list):
    item_name_list_copy = list(item_name_list)
    random.shuffle(item_name_list_copy)
    ranking_dict = {}
    for i in range(len(item_name_list_copy)):
        ranking_dict[item_name_list_copy[i]] = i
    return ranking_dict


# ranks elo
def generate_ranking_dict_elo(item_name_list, item_preference_ab_list):
    elo_rating_dict = compute_elo_rating_dict(item_name_list, item_preference_ab_list)
    item_name_elo_list = sorted(elo_rating_dict.items(), key=operator.itemgetter(1))
    ranking_dict = {}
    for i in range(len(item_name_elo_list)):
        ranking_dict[item_name_elo_list[i][0]] = i
    return ranking_dict

def compute_elo_rating_dict(item_name_list, item_preference_ab_list):
    elo_rating_dict = {}
    for item_name in item_name_list:
        elo_rating_dict[item_name] = 1500

    for item_preference_ab in item_preference_ab_list:
        update_elo_rating(elo_rating_dict, item_preference_ab)
    return elo_rating_dict

def update_elo_rating(elo_rating_dict, item_preference_ab):
    item_name_a = item_preference_ab[0]
    item_name_b = item_preference_ab[1]
    Sa = 1
    Sb = 0
    if item_preference_ab[2]:
        Sa = 0
        Sb = 1
    K = 16
    Ra = elo_rating_dict[item_name_a]
    Rb = elo_rating_dict[item_name_b]
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
    elo_rating_dict[item_name_a] = Ra + K * (Sa - Ea)
    elo_rating_dict[item_name_b] = Rb + K * (Sb - Eb)
