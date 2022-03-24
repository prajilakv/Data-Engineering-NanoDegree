import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events
        (
            artist          VARCHAR(500),
            auth            VARCHAR,
            first_name      VARCHAR,
            gender          VARCHAR,
            item_in_session INTEGER,
            last_name       VARCHAR,
            length          FLOAT,
            level           VARCHAR,
            location        VARCHAR(1000),
            method          VARCHAR,
            page            VARCHAR,
            registration    BIGINT,
            session_id      INTEGER,
            song            VARCHAR,
            status          INTEGER,
            ts              BIGINT,
            user_agent      VARCHAR(1000),
            user_id         INT
        )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
        (
            song_id             VARCHAR,
            title               VARCHAR(500),
            duration            FLOAT,
            year                INTEGER,
            artist_id           VARCHAR,
            artist_name         VARCHAR(500),
            artist_latitude     FLOAT,
            artist_longitude    FLOAT,
            artist_location     VARCHAR(1000),
            num_songs           INTEGER
        )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay
    (
        songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY, 
        start_time TIMESTAMP NOT NULL SORTKEY, 
        user_id INT NOT NULL DISTKEY, 
        level VARCHAR, 
        song_id VARCHAR, 
        artist_id VARCHAR, 
        session_id INTEGER, 
        location VARCHAR(1000), 
        user_agent VARCHAR(1000)
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id INT PRIMARY KEY, 
        first_name VARCHAR, 
        last_name VARCHAR, 
        gender VARCHAR, 
        level VARCHAR
    )
    diststyle auto
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song
    (
        song_id VARCHAR PRIMARY KEY SORTKEY, 
        title VARCHAR(500), 
        artist_id VARCHAR DISTKEY, 
        year INTEGER, 
        duration FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist
    (
        artist_id VARCHAR PRIMARY KEY, 
        name VARCHAR(500), 
        location VARCHAR(1000), 
        lattitude FLOAT, 
        longitude FLOAT
    )
    diststyle all
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time TIMESTAMP PRIMARY KEY SORTKEY, 
        hour INTEGER, 
        day INTEGER, 
        week INTEGER, 
        month INTEGER, 
        year INTEGER DISTKEY, 
        weekday INTEGER
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY {} 
    FROM {}
    IAM_ROLE '{}'
    JSON {} 
    region '{}';
""").format(
    'staging_events',
    config['S3']['LOG_DATA'],
    config['IAM_ROLE']['ARN'],
    config['S3']['LOG_JSONPATH'],
    config['CLUSTER']['REGION'],
    )

staging_songs_copy = ("""
    COPY {} 
    FROM {}
    IAM_ROLE '{}'
    JSON 'auto' 
    region '{}';
""").format(
    'staging_songs',
    config['S3']['SONG_DATA'],
    config['IAM_ROLE']['ARN'],
    config['CLUSTER']['REGION'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT  
        timestamp 'epoch' + se.ts/1000 * interval '1 second',
        se.user_id, 
        se.level, 
        ss.song_id, 
        ss.artist_id, 
        se.session_id, 
        se.location, 
        se.user_agent
    FROM staging_events se
    JOIN staging_songs ss
        ON se.song = ss.title
        AND se.artist = ss.artist_name
        WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users(user_id,first_name, last_name, gender, level)
    SELECT DISTINCT
        user_id,
        first_name, 
        last_name, 
        gender, 
        level
    FROM staging_events
    WHERE user_id IS NOT NULL
""")

song_table_insert = ("""
    INSERT INTO song(song_id, title, artist_id, year, duration)
    SELECT DISTINCT
        song_id, 
        title, 
        artist_id, 
        year, 
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
        
""")

artist_table_insert = ("""
    INSERT INTO artist(artist_id, name, location, lattitude, longitude)
    SELECT DISTINCT 
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
    SELECT 
        timestamp 'epoch' + ts/1000 * interval '1 second' as st, 
        extract(hour from st),
        extract(day from st),
        extract(week from st), 
        extract(month from st),
        extract(year from st), 
        extract(dayofweek from st)
    FROM staging_events
""")


# Count Test queries
songplay_table_count = ("""
    SELECT COUNT(*) FROM songplay as songplay_count
""")

song_table_count = ("""
    SELECT COUNT(*) FROM song as song_count
""")

user_table_count = ("""
    SELECT COUNT(*) FROM users as user_count
""")

artist_table_count = ("""
    SELECT COUNT(*) FROM artist as artist_count
""")

time_table_count = ("""
    SELECT COUNT(*) FROM time as timeg_count
""")




# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
test_queries=[songplay_table_count, user_table_count, song_table_count, artist_table_count, time_table_count]
