# Suggesting to use WSGI server.
# If you are using API in your local machine you can use
#
#

from flask import Flask, jsonify, request
from ensta import Host, SessionHost, Guest
from api_funcs import login_required

app = Flask(__name__)




@app.route('/login', methods=['POST'])
def login():
    # try:
    data = request.json
    username = data.get('username')
    password = data.get('password')
    two_factor = data.get('two_factor')
    proxy = data.get('proxy')
    print(username, password, two_factor, proxy)

    host = Host(username=username, password=password, totp_token=two_factor, proxy=proxy)


    return jsonify({'status': 'ok', 'session_data': host.session_data})

    # except Exception as e:
    #     return jsonify({
    #         'status': 'fail',
    #         'message': str(e)
    #     })


@app.route('/uploadImage', methods=['POST'])
@login_required
def uploadImage():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        caption = data.get('caption')
        pic_url = data.get('picture')
        proxy = data.get('proxy')

        if caption == '' or caption is None or caption.isspace():
            caption = ""

        if pic_url is None:
            return jsonify({'status': 'fail', 'message': 'Picture URL is required'}), 400

        host = SessionHost(session_data_str, proxy=proxy)
        upload = host.get_upload_id(pic_url)
        host.upload_photo(upload, caption)

        return jsonify({'status': 'ok', 'message': 'Image uploaded successfully'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': str(e)
        })


@app.route('/uploadMultipleImage', methods=['POST'])
@login_required
def uploadMultipleImage():
    """
    Upload multiple image in a single post
    :return: None
    """
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        caption = data.get('caption')
        pics_url = request.files.getlist('pictures')
        proxy = data.get('proxy')

        if caption == '' or caption is None or caption.isspace(): caption = ""

        if pics_url is None:
            return jsonify({'status': 'fail', 'message': 'Picture URL is required'}), 400

        upload_ids = list()
        host = SessionHost(session_data_str, proxy=proxy)
        for pic in pics_url:
            upload_id = host.get_upload_id(pic.filename)
            upload_ids.append(upload_id)

        host.upload_photos(upload_ids, caption=caption)

        return jsonify({'status': 'ok', 'message': 'Images uploaded successfully'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': str(e)
        })


@app.route('/uploadReels', methods=['POST'])
@login_required
def uploadReels():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        thumbnail_path = data.get('thumbnail')
        caption = data.get('caption')
        video_path = data.get('video_path')
        proxy = data.get('proxy')

        host = SessionHost(session_data_str, proxy=proxy)
        host.upload_reel(
            video_path=video_path,
            thumbnail_path=thumbnail_path,
            caption=caption
        )
        return jsonify({'status': 'ok', 'message': 'Reels uploaded successfully'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/checkUsernameAvailability', methods=['POST'])
def checkUsernameAvailability():

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')

        guest = Guest(proxy=proxy)
        result = guest.username_availability(username)

        return jsonify({'status': 'ok', 'result': result})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


# Will be done in a few days
@app.route('/fetchProfileData', methods=['POST'])
@login_required
def fetchProfileData():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        save_file = True

        host = SessionHost(session_data_str, proxy=proxy)
        profile = host.profile(username=username)

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })

    return jsonify({'status': 'ok', 'profile_data': profile})

if __name__ == "__main__":
    # Change debug mode False if you are not going to debug app.
    app.run(debug=True)
