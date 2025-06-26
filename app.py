from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

DATA_FILE = 'submissions.csv'

# Create CSV file with header if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Hobby', 'Food', 'Vacation', 'Animal', 'Movie', 'Job'])

# Mapping logic
def generate_music_plan(submission):
    name, hobby, food, vacation, animal, movie, job = submission

    # Map food to Pitch
    food_pitch_map = {
        'pizza': 'C',
        'sushi': 'A',
        'burger': 'G',
        'pasta': 'F',
        'salad': 'E'
    }
    pitch = food_pitch_map.get(food.lower(), 'C')

    # Map hobby to Rhythm
    hobby_rhythm_map = {
        'reading': 'Slow Waltz 3/4',
        'dancing': 'Fast Syncopation',
        'sports': 'Steady 4/4',
        'painting': 'Irregular 5/4',
        'coding': 'Steady 4/4'
    }
    rhythm = hobby_rhythm_map.get(hobby.lower(), 'Steady 4/4')

    # Map vacation to Melody
    vacation_melody_map = {
        'beach': 'Leaping Melody',
        'mountains': 'Ascending Stepwise',
        'city': 'Minor Scales',
        'forest': 'Descending Intervals'
    }
    melody = vacation_melody_map.get(vacation.lower(), 'Ascending Stepwise')

    # Map animal to Timbre
    animal_timbre_map = {
        'dog': 'Flute',
        'cat': 'Electric Guitar',
        'bird': 'Violin',
        'lion': 'Trumpet'
    }
    timbre = animal_timbre_map.get(animal.lower(), 'Violin')

    # Map movie to Form
    movie_form_map = {
        'inception': 'Theme & Variations',
        'titanic': 'ABA (ternary)',
        'avengers': 'Rondo',
        'frozen': 'Verse-Chorus'
    }
    form = movie_form_map.get(movie.lower(), 'Verse-Chorus')

    # Map job to Tempo
    job_tempo_map = {
        'scientist': '60 BPM (Adagio)',
        'teacher': '120 BPM (Moderato)',
        'athlete': '160 BPM (Allegro)',
        'singer': '200 BPM (Presto)'
    }
    tempo = job_tempo_map.get(job.lower(), '120 BPM (Moderato)')

    # Map pitch to simple lyrics
    lyric_map = {
        'C': '"I feel alive in the sunshine"',
        'A': '"Tears fall like rain tonight"',
        'G': '"We rise like mountains"',
        'F': '"The stars will guide me home"',
        'E': '"Lost in a storm of doubt"'
    }
    lyrics = lyric_map.get(pitch, '"I feel alive in the sunshine"')

    return {
        'Pitch': pitch,
        'Rhythm': rhythm,
        'Melody': melody,
        'Timbre': timbre,
        'Form': form,
        'Tempo': tempo,
        'Lyrics': lyrics
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        hobby = request.form.get('hobby')
        food = request.form.get('food')
        vacation = request.form.get('vacation')
        animal = request.form.get('animal')
        movie = request.form.get('movie')
        job = request.form.get('job')

        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, hobby, food, vacation, animal, movie, job])

        return render_template('result.html', name=name)
    return render_template('form.html')

@app.route('/submissions')
def submissions():
    all_submissions = []
    generated_plans = []

    with open(DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            all_submissions.append(row)
            plan = generate_music_plan(row)
            generated_plans.append(plan)

    return render_template('submissions.html', submissions=all_submissions, plans=generated_plans)

if __name__ == '__main__':
    app.run(debug=True)
