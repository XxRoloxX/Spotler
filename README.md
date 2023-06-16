# Spotler
<!DOCTYPE html>
<html>

<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.5;
    }

    h1 {
      color: #333;
      font-size: 24px;
    }

    h2 {
      color: #555;
      font-size: 20px;
    }

    p {
      color: #777;
      font-size: 16px;
    }

    code {
      background-color: #f4f4f4;
      padding: 4px 8px;
      border-radius: 4px;
    }

    pre {
      background-color: #f4f4f4;
      padding: 12px;
      border-radius: 4px;
      overflow-x: auto;
    }
  </style>
</head>

<body>
  <h1>spotler-api🎵</h1>

  <p>
    This Django microservice provides an efficient way to collect large datasets required for training classification models
    using the Spotify Web API. It automates the process of authenticating and retrieving metadata about tracks and artists,
    allowing uninterrupted data collection over an extended period.
  </p>

  <h3>Installation ⚙️</h3>

  <ol>
    <li>Clone the repository:
      <pre><code>git clone https://github.com/Xx_Rolo_xX/spotler-api.git</code></pre>
    </li>
    <li>Change into the project directory:
      <pre><code>cd spotler-api</code></pre>
    </li>
    <li>Create and activate a virtual environment (recommended):
      <pre><code>python3 -m venv venv
        source venv/bin/activate</code></pre>
    </li>
    <li>Install the required dependencies:
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Set up the database:
      <pre><code>python manage.py migrate</code></pre>
    </li>
    <li>Run the microservice:
      <pre><code>python manage.py runserver</code></pre>
    </li>
  </ol>

  <h3>Authentication 🔒</h3>

  <p>
    To access the Spotify Web API, you need to provide a valid access token. This microservice handles authentication
    automatically and ensures uninterrupted data retrieval by automatically refreshing the access token before it expires.
  </p>

  <h3>Endpoints 🛠️</h3>

  <p>
    The microservice exposes the following endpoints for data retrieval:
  </p>

  <ol>
    <li><code>/tracks</code>: Retrieve basic information about a track, including its identifier, name, and artist(s)
      associated with the track.</li>
    <li><code>/artists</code>: Retrieve basic information about an artist based on their identifier, including the artist's
      name and associated genres.</li>
    <li><code>/audio-features</code>: Retrieve metadata about a track based on its identifier, including features like
      acousticness, danceability, energy, instrumentalness, key, loudness, liveness, mode, speechiness, tempo, time
      signature, and valence.</li>
    <li><code>/playlists</code>: Retrieve the track identifiers from a specific user's playlist.</li>
    <li><code>/users/{user_id}/playlists</code>: Retrieve playlists belonging to a specific user.</li>
  </ol>

  <h3>Data Management 🗃️</h3>

  <p>
    The microservice utilizes a RESTful architecture to handle data collection efficiently. Upon receiving a GET request
    with a playlist identifier, the microservice retrieves data for all tracks in the playlist, stores it in a SQLite
    relational database, and applies the appropriate data schema for tracks, artists, and genres.
  </p>

  <p>
    The advantages of this approach include eliminating entries for artists without associated genres and ensuring data
    integrity through database validations.
  </p>

  <h3>Data Source 🎧</h3>

  <p>
    The analyzed tracks are sourced from over 800 playlists belonging to a Spotify user's official account. These playlists
    were chosen for their diversity and centralized around a single user, guaranteeing a vast and diverse dataset while
    mitigating biases from private users.
  </p>

  <h3>Data Structure 📊</h3>

  <p>
    The collected dataset adheres to the following principles:
  </p>

  <ol>
    <li>Each track is associated with at least one artist.</li>
    <li>Each artist can be associated with any number of genres.</li>
    <li>Each track possesses a set of metadata, including features such as acousticness, danceability, energy,
      instrumentalness, key, loudness, liveness, mode, speechiness, tempo, time signature, and valence.</li>
  </ol>

  <h3>Contribution 🤝</h3>

  <p>
    Contributions to this microservice are welcome. If you encounter any issues or have suggestions for improvement, please
    submit an issue or a pull request.
  </p>

  <h3>License 📝</h3>

  <p>
    This project is licensed under the <a href="https://opensource.org/licenses/MIT">MIT License</a>.
  </p>

</body>

</html>
