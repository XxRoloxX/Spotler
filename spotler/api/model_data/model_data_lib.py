import pprint
import sqlite3
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from spotler.api.data_collection.data_clean_up import get_clean_track_data, get_sql_query_results

TRACK_SIMPLE_GENRE_SQL_QUERY =  '''SELECT api_track.*, api_genre.simplyfied_name FROM api_track
    INNER JOIN api_track_artists ON api_track.track_id = api_track_artists.track_id
    INNER JOIN api_artist_genres ON api_track_artists.artist_id=api_artist_genres.artist_id 
    INNER JOIN api_genre ON api_artist_genres.genre_id=api_genre.id 
    WHERE api_genre.simplyfied_name IS NOT NULL'''

TRACK_GENRE_SQL_QUERY =  '''SELECT api_track.*, api_genre.name as genre_name FROM api_track
    INNER JOIN api_track_artists ON api_track.track_id = api_track_artists.track_id
    INNER JOIN api_artist_genres ON api_track_artists.artist_id=api_artist_genres.artist_id 
    INNER JOIN api_genre ON api_artist_genres.genre_id=api_genre.id 
    WHERE api_genre.name IS NOT NULL'''




def create_csv_from_query(db_path, csv_filename, query,separator:str):
    
    query_results, cur = get_sql_query_results(db_path,query)
    
    column_names = [name[0] for name in cur.description]
    print(column_names)

    with open(csv_filename, "w", encoding="UTF-8") as csv_file:
        csv_file.write(separator.join(column_names))
        csv_file.write("\n")
        for row in query_results:
            row_stringified = map(lambda data: str(data),row)
            csv_file.write(separator.join(row_stringified))
            csv_file.write("\n")
    
    cur.close()
    return column_names

def fit_data_to_lda(db_path, inclusion_criteria):
    

    def get_predicted_genres(classes, result_prob):
        
        result = [{"genre":prob_class, "probability":prob_value} for prob_class, prob_value in zip(classes, result_prob[0]) if prob_value>inclusion_criteria]
        result.sort(key=lambda el: el["probability"], reverse=True)               
        return result

    clean_track_data = get_clean_track_data(db_path)
    metadata = np.array(list(map(lambda track: [*track[2:-1]],clean_track_data)))
    genres = np.array(list(map(lambda track: track[-1], clean_track_data)))

    pprint.pprint(metadata)
    pprint.pprint(genres)

    X_train, X_test, Y_train, Y_test = train_test_split(metadata, genres, test_size=0.2, random_state=42, stratify=genres)

    clf = LinearDiscriminantAnalysis()
    clf.fit_transform(X_train,Y_train)
    correct_guesses=0


    for x_test, y_test in zip(X_test,Y_test):

        predicted_probalities = get_predicted_genres(clf.classes_, clf.predict_proba([x_test]))
        predicted_genre = clf.predict([x_test])[0]
        pprint.pprint("Test value "+str(y_test))
        pprint.pprint(predicted_probalities)
        

        if y_test in [genre["genre"] for genre in predicted_probalities]:
            correct_guesses+=1

    return correct_guesses/len(X_test),inclusion_criteria


