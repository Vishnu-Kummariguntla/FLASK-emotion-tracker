from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage of submitted data (cleared on restart)
submitted_data = []

# Cricket archetype mapping
website_to_cricket_archetype = {
    "cricviz.com": "Strategist – Spin Bowler",
    "espncricinfo.com/analysis": "Strategist – Spin Bowler",
    "wikipedia.org": "Strategist – Spin Bowler",
    "reddit.com/r/Cricket": "Blazer – T20 Batter",
    "cricbuzz.com": "Blazer – T20 Batter",
    "bbc.com/sport/cricket": "Shield – Test Batter",
    "espn.com": "Enforcer – Fast Bowler",
    "notion.so": "Analyst – Wicketkeeper",
    "tradingview.com": "Finisher – Middle-Order",
    "duolingo.com": "Shape-Shifter – All-Rounder",
    "tripadvisor.com": "Watcher – Outfielder"
}

# Star Wars archetype mapping
website_to_star_wars_archetype = {
    "plato.stanford.edu": "Green – The Sage",
    "ted.com/talks": "Green – The Sage",
    "wikipedia.org": "Blue – The Guardian",
    "un.org": "Blue – The Guardian",
    "4chan.org": "Red – The Rebel",
    "hackforums.net": "Red – The Rebel",
    "reddit.com": "Purple – The Maverick",
    "quora.com": "Purple – The Maverick",
    "headspace.com": "White – The Redeemed",
    "calm.com": "White – The Redeemed",
    "eff.org": "Yellow – The Sentinel",
    "archive.org": "Yellow – The Sentinel"
}

def categorize_urls(urls, mapping):
    role_count = {}
    for url in urls:
        if not url:
            continue
        for known_site in mapping:
            if known_site in url:
                role = mapping[known_site]
                role_count[role] = role_count.get(role, 0) + 1
                break
    return max(role_count.items(), key=lambda x: x[1])[0] if role_count else "Uncategorized"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = [
            request.form.get('url1'),
            request.form.get('url2'),
            request.form.get('url3'),
            request.form.get('url4'),
            request.form.get('url5'),
        ]

        cricket_archetype = categorize_urls(urls, website_to_cricket_archetype)
        star_wars_archetype = categorize_urls(urls, website_to_star_wars_archetype)

        form_data = {
            'name': request.form.get('name'),
            'hobby': request.form.get('hobby'),
            'food': request.form.get('food'),
            'vacation': request.form.get('vacation'),
            'animal': request.form.get('animal'),
            'movie': request.form.get('movie'),
            'job': request.form.get('job'),
            'urls': urls,
            'cricket_archetype': cricket_archetype,
            'star_wars_archetype': star_wars_archetype
        }

        submitted_data.append(form_data)
        return redirect(url_for('results'))

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', submissions=submitted_data)

if __name__ == '__main__':
    app.run(debug=True)
