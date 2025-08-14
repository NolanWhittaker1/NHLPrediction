import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier

df = pd.read_csv('generated_data/ml_shaped_data.csv')
df['home_or_away'] = df['home_or_away'].map({"HOME":0})
for i in range(3, 11):
    depth = i
    print("Depth: ", depth)
    rf_model = make_pipeline(
        RandomForestClassifier(n_estimators=250, max_depth=depth, min_samples_leaf=7)
    )
    
    grad_model = make_pipeline(
        GradientBoostingClassifier(n_estimators=250,max_depth=depth, min_samples_leaf=7)
    )
    
    models = [rf_model, grad_model]
    
    for model in models:
        training_data = df[df['season'] != 2024]
        valid_data = df[df['season'] == 2024]
        valid_data = valid_data.sort_values(by=['season', 'gameDate'])
        X_train = training_data.drop(columns=['playerTeam','opposingTeam','win'])
        y_train = training_data['win']
        model.fit(X_train, y_train)
        print(model.score(valid_data.drop(columns=['playerTeam','opposingTeam','win']), valid_data['win']))
        #print(model)
    print()

'''
for i in range(2008, 2024):
    rf_model = make_pipeline(
        RandomForestClassifier(n_estimators=250, max_depth=3, min_samples_leaf=7)
    )
    
    grad_model = make_pipeline(
        GradientBoostingClassifier(n_estimators=250,max_depth=3, min_samples_leaf=7)
    )
    
    models = [rf_model, grad_model]
    print(i)
    for model in models:
        training_data = df[df['season'] != i]
        valid_data = df[df['season'] == i]
        valid_data = valid_data.sort_values(by=['season', 'gameDate'])
        X_train = training_data.drop(columns=['playerTeam','opposingTeam','win'])
        y_train = training_data['win']
        model.fit(X_train, y_train)
        print(model.score(valid_data.drop(columns=['playerTeam','opposingTeam','win']), valid_data['win']))
       
    print()
'''

    





