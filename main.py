from playerdata import *
import os
from datetime import datetime
import shutil


if __name__ == '__main__':
    a = datetime.now()
    shutil.rmtree("jsons_old")
    os.rename('jsons_new','jsons_old')
    os.mkdir('jsons_new')
    os.remove("old_data.sqlite")
    os.rename("new_data.sqlite","old_data.sqlite")
    #os.remove("players.sqlite")
    #getchallengers() 
    getmatchids(10)
    getchampinfo()
    gettraitinfo() 
    getcompinfo() 
    parsechampdata() 
    parsetraitdata() 
    parsecompdata()
    os.remove("popularity_scores/champ_scores_old.json") 
    os.rename("popularity_scores/champ_scores_new.json","popularity_scores/champ_scores_old.json") 
    os.remove("popularity_scores/trait_scores_old.json") 
    os.rename("popularity_scores/trait_scores_new.json","popularity_scores/trait_scores_old.json") 
    os.remove("popularity_scores/comp_scores_old.json") 
    os.rename("popularity_scores/comp_scores_new.json","popularity_scores/comp_scores_old.json") 
    getchampscore() 
    gettraitscore() 
    getcompscore() 
    parsechampscore() 
    parsetraitscore() 
    parsecompscore() 
    b = datetime.now()
    print("total time :", b - a)
