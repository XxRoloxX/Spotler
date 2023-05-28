import pprint
import sqlite3
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

def get_most_popular_genres(n, db_path):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
    '''SELECT api_genre.name, COUNT(api_genre.id) as q FROM api_track
    INNER JOIN api_track_artists ON api_track.track_id = api_track_artists.track_id
    INNER JOIN api_artist_genres ON api_track_artists.artist_id=api_artist_genres.artist_id
    INNER JOIN api_genre ON api_artist_genres.genre_id=api_genre.id
    GROUP BY api_genre.name
    ORDER BY q DESC LIMIT (?)''', (n,))

    result = cur.fetchall()
    cur.close()
    return result

def get_clean_track_data(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
    '''SELECT api_track.*, api_genre.simplyfied_name FROM api_track
    INNER JOIN api_track_artists ON api_track.track_id = api_track_artists.track_id
    INNER JOIN api_artist_genres ON api_track_artists.artist_id=api_artist_genres.artist_id 
    INNER JOIN api_genre ON api_artist_genres.genre_id=api_genre.id 
    WHERE api_genre.simplyfied_name IS NOT NULL''')

    result = cur.fetchall()
    cur.close()
    return result

def get_tracks_without_artists(db_path):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''SELECT api_track.track_id, COUNT(api_track_artists.artist_id) as q 
    FROM api_track 
    LEFT JOIN api_track_artists ON api_track.track_id=api_track_artists.track_id 
    GROUP BY api_track.track_id 
    HAVING q=0
    ''')
    tracks = cur.fetchall()
    return tracks


def remove_tracks_without_artists(db_path):

    tracks = get_tracks_without_artists(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for track in tracks:
        cur.execute('''DELETE FROM api_track WHERE api_track.track_id=(?)''',(track[0],))
    
    rowcount = cur.rowcount
    conn.commit()
    cur.close()
    return rowcount

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


if __name__=="__main__":
    print(remove_tracks_without_artists("db.sqlite3"))