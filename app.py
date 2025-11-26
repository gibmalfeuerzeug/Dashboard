from flask import Flask, session, redirect, request, render_template, jsonify
import requests
import os
from urllib.parse import urlencode
from database import get_guild, set_prefix, get_or_create_guild
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

app = Flask(__name__)
app.secret_key = SECRET_KEY


# --- Login ---
@app.route('/login')
def login():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'identify guilds'
    }
    return redirect("https://discord.com/api/oauth2/authorize?" + urlencode(params))


# --- Callback ---
@app.route('/callback')
def callback():
    code = request.args.get('code')

    token = requests.post(
        'https://discord.com/api/oauth2/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    ).json()

    access = token['access_token']

    user = requests.get(
        'https://discord.com/api/users/@me',
        headers={"Authorization": f"Bearer {access}"}
    ).json()

    guilds = requests.get(
        'https://discord.com/api/users/@me/guilds',
        headers={"Authorization": f"Bearer {access}"}
    ).json()

    session['user'] = user
    session['guilds'] = guilds

    return redirect('/')


# --- Index ---
@app.route('/')
def index():
    return render_template(
        'index.html',
        user=session.get('user'),
        guilds=session.get('guilds')
    )


# --- Guild Dashboard ---
@app.route('/guild/<gid>')
def guild_page(gid):
    guilds = session.get('guilds') or []

    if not any(g['id'] == gid for g in guilds):
        return "Keine Berechtigung", 403

    guild = get_or_create_guild(gid)
    return render_template('guild.html', guild=guild)


# --- Prefix ändern ---
@app.route('/api/set_prefix/<gid>', methods=['POST'])
def api_set_prefix(gid):
    prefix = request.json.get('prefix')
    set_prefix(gid, prefix)
    return jsonify({'success': True, 'prefix': prefix})


app.run(port=3000)
