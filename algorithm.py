import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_excel(r"C:\Users\abelf\Downloads\final_heart_rate_data.xlsx")

#Predictions = []

def regr(features, Predictions):
        for dct in features:
             
            lst_keys = list(dct.keys())
            lst_values = list(dct.values())

            

            x = data[["tempo","acousticness","danceability","energy","instrumentalness","liveness","loudness","valence"]]
            y = data[["interval 4-HR"]]
            X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.33, random_state=42)
            reg = LinearRegression().fit(X_train, y_train)
            tempo_index = lst_keys.index("tempo")
            loudness_index = lst_keys.index("loudness")
            speechiness_index = lst_keys.index("speechiness")
            acousticness_index = lst_keys.index("acousticness")
            instrumentalness_index = lst_keys.index("instrumentalness")
            energy_index = lst_keys.index("energy")
            valence_index = lst_keys.index("valence")
            danceability_index = lst_keys.index("danceability")
            liveness_index = lst_keys.index("liveness")

            Predictions.append(reg.predict([[lst_values[tempo_index],lst_values[acousticness_index],lst_values[danceability_index],lst_values[energy_index],lst_values[instrumentalness_index],lst_values[liveness_index],lst_values[loudness_index],lst_values[valence_index]]]))

        return Predictions
        