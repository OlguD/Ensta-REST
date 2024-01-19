# Suggesting to use WSGI server.
# 
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


@app.route('/username-to-userid', methods=['POST'])
def username_to_user_id():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        uid = host.get_uid(username)

        return jsonify({'status': 'ok', 'user_id': uid})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/followUser', methods=['POST'])
def followUser():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        host.follow(username)

        return jsonify({'status': 'ok', 'result': f'-- Following {username}'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/unfollowUser', methods=['POST'])
def followUser():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        host.unfollow(username)

        return jsonify({'status': 'ok', 'result': f'-- Unfollowed {username}'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/getFollowerList', methods=['POST'])
def getFollowerList():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        followers = host.followers(username, count=0)

        return jsonify({'status': 'ok', 'result': followers})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/getFollowingList', methods=['POST'])
def getFollowerList():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        username = data.get('username')
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        followings = host.followings(username, count=0)

        return jsonify({'status': 'ok', 'result': followings})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/switchToPublic', methods=['POST'])
def switchToPublic():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        host.switch_to_public_account()

        return jsonify({'status': 'ok', 'result': 'Account switched to public'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/switchToPrivate', methods=['POST'])
def switchToPrivate():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        proxy = data.get('proxy')
        host = SessionHost(session_data_str, proxy=proxy)
        host.switch_to_private_account()

        return jsonify({'status': 'ok', 'result': 'Account switched to private'})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/fetchSomeonesFeed', methods=['POST'])
def fetchSomeonesFeed():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        proxy = data.get('proxy')
        username = data.get('username')
        host = SessionHost(session_data_str, proxy=proxy)

        posts = host.posts(username, count=0)

        return jsonify({'status': 'ok', 'posts': posts})

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


@app.route('/addComment', methods=['POST'])
def addComment():
    with open('ensta-session.txt', 'r') as file:
        session_data_str = file.read()

    try:
        data = request.json
        post_link = data.get('post_link')
        comment = data.get('comment')
        proxy = data.get('proxy')

        host = SessionHost(session_data_str, proxy=proxy)

        post_id = host.get_post_id(post_link)
        host.comment(comment, post_id)

        return jsonify({
            'status': 'ok',
            'result': f'Added comment to {post_link}'
        })

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': e
        })


if __name__ == "__main__":
    # Change debug mode False if you are not going to debug app.
    app.run(debug=True)