from pymongo import MongoClient
from random import randint
import gridfs


# TODO:gestisci passaggio di parametri con file di configurazione

def rundb():
    _client = MongoClient('mongodb://127.0.0.1:27017')
    db = _client.UserProfileManagerDB


def get_random_user(col):
    return col.users.find_one()


# TODO: ricorda di gestire id di user mobility profile main logic differente dal db
def read_field_from_ump(user_id, col, field):
    return col.users.find_one({'_id': user_id}, {field: 1, '_id': 0})


def read_all_from_ump(user_id, col):
    return col.users.find_one({'_id': user_id})


def modify_to_ump(user_id, col, field, value):
    return col.users.update_one({'_id': user_id},
                                {'$set': {field: value}})


def read_all_users(col):
    return col.users.find({})


def insert_user(col, value):
    return col.users.insert_one(value)  # Return the ID


def delete_user(user_id, col):
    return col.users.delete_one({'_id': user_id})


def insert_image(db, image, user_id):
    image_id = insert_file(db, image)
    return modify_to_ump(user_id, db, 'image', image_id)


def insert_audio(db, audio, user_id):
    audio_id = insert_file(db, audio)
    return modify_to_ump(user_id, db, 'audio', audio_id)


def get_image_by_id(db, user_id):
    fs = gridfs.GridFS(db)
    image_id = read_field_from_ump(user_id, db, 'image')
    if image_id:
        return fs.get(image_id['image']).read()

    return 1


def get_audio_by_id(db, user_id):
    fs = gridfs.GridFS(db)
    audio_id = read_field_from_ump(user_id, db, 'audio')
    if audio_id:
        out = fs.get(audio_id['audio']).read()
        output = open(str(user_id) + '.mp3', 'wb')
        output.write(out)
        output.close()

    return 1


def insert_file(db, file):
    fs = gridfs.GridFS(db)
    data = open(file, 'rb')
    the_data = data.read()
    stored = fs.put(the_data)

    return stored


def get_all_images(col):
    users = col.users.find().distinct('_id')
    try:
        for user in users:
            out = get_image_by_id(col, user)
            if out is not 1:
                output = open(str(user) + '.jpg', 'wb')
                output.write(out)
                output.close()
    except:
        return 1

    return 0


def get_all_audio(col):
    users = col.users.find().distinct('_id')
    try:
        for user in users:
            get_audio_by_id(col, user)
    except:
        return 1

    return 0


def create_user(db, user):
    return db.users.insert_one(user)


def create_user_json(user):  # Use it only for test
    user_profile_manager_db = {
        'Name': user[0],
        'surname': user[1],
        'gender': user[2],
        'age': user[3],
        'country': user[4],
        'home_location': user[5],
        'job_location': user[6],
        'driving_style': user[7],
        'seat_inclination': user[8],
        'seat_orientation': user[9],
        'temperature_level': user[10],
        'light_level': user[11],
        'music_genres': user[12],
        'music_volume': user[13],
        # 'application_list': application_list[randint(0, (len(application_list) - 1))],
        # 'service_list': service_list[randint(0, (len(service_list) - 1))]
    }

    return user_profile_manager_db


def populate_db():
    client = MongoClient('mongodb://127.0.0.1:27017')  # Open DB
    db = client.UserProfileManagerDB  # Define DB

    mycol = db["users"]  # Get collection
    mycol.drop()  # Clean collection

    names = ['Guido', 'Federico', 'Riccardo', 'Daria', 'Marsha', 'Andrea']
    surname = ['Bertini', 'Lapenna']
    gender = ['Male', 'Female']
    age = [25, 28, 22, 23]
    country = ['Italian', 'Puerto Rico']
    home_location = ['Campo', 'Ozieri']
    job_location = ['none']
    driving_style = ['Sport', 'Normal']
    seat_inclination = [30, 31, 32, 27]
    seat_orientation = ['Frontal']
    temperature_level = [25, 26, 27, 28, 29]
    light_level = ['low', 'medium', 'high']
    music_genres = ['Metal', 'rap']
    music_volume = ['moderate', 'high']
    application_list = ['Facebook', 'youtube']
    service_list = ['Amazon prime', 'Netflix']

    for x in range(1, 3):
        user_profile_manager_db = {
            'Name': names[randint(0, (len(names) - 1))],
            'surname': surname[randint(0, (len(surname) - 1))],
            'gender': gender[randint(0, (len(gender) - 1))],
            'age': age[randint(0, (len(age) - 1))],
            'country': country[randint(0, (len(country) - 1))],
            'home_location': home_location[randint(0, (len(home_location) - 1))],
            'job_location': job_location[randint(0, (len(job_location) - 1))],
            'driving_style': driving_style[randint(0, (len(driving_style) - 1))],
            'seat_inclination': seat_inclination[randint(0, (len(seat_inclination) - 1))],
            'seat_orientation': seat_orientation[randint(0, (len(seat_orientation) - 1))],
            'temperature_level': temperature_level[randint(0, (len(temperature_level) - 1))],
            'light_level': light_level[randint(0, (len(light_level) - 1))],
            'music_genres': music_genres[randint(0, (len(music_genres) - 1))],
            'music_volume': music_volume[randint(0, (len(music_volume) - 1))],
            'application_list': application_list,
            'service_list': service_list
        }
        # Step 3: Insert business object directly into MongoDB via isnert_one
        result = db.users.insert_one(user_profile_manager_db)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created {0} of 500 as {1}'.format(x, result.inserted_id))
    # Step 5: Tell us that you are done
    print('finished creating 500 business reviews')
