from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request, 
    Response, 
    send_file, jsonify, 
    send_from_directory
)
from flask import Flask, render_template, request, Response, send_file, redirect, url_for, jsonify, send_from_directory
import base64
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from models import Photos
from models import Camera_Parameters
from forms import login_form,register_form
from sqlalchemy.sql.expression import func
from sqlalchemy import select

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



from datetime import datetime


def retrieve_photos_by_album_id_within_date_range(album_id, begin_date_str, end_date_str):
    photos = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT photo_data
            FROM photos
            WHERE album_id = %s
            AND date_taken BETWEEN %s AND %s
            ORDER by date_taken DESC
        """
         
        # Convert date strings to datetime.date objects
        begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Set time to midnight for the beginning of the day
        formatted_begin_date = datetime.combine(begin_date, time.min).strftime('%Y-%m-%d %H:%M:%S')
        # Set time to just before midnight for the end of the day
        formatted_end_date = datetime.combine(end_date, time.max).strftime('%Y-%m-%d %H:%M:%S')
    

        print("Parsed Begin Date:", begin_date)
        print("Parsed End Date:", end_date)
        print("Formatted Begin Date:", formatted_begin_date)
        print("Fformatted End Date:", formatted_end_date)
       
        cursor.execute(query, (album_id, formatted_begin_date, formatted_end_date))
        photos = cursor.fetchall()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        cnx.close()
    return photos

def retrieve_HD1080p_by_album_id_within_date_range(album_id, begin_date_str, end_date_str):
    photos = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT HD1080p_data
            FROM photos
            WHERE album_id = %s
            AND date_taken BETWEEN %s AND %s
            ORDER by date_taken ASC
        """
         
        # Convert date strings to datetime.date objects
        begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Set time to midnight for the beginning of the day
        formatted_begin_date = datetime.combine(begin_date, time.min).strftime('%Y-%m-%d %H:%M:%S')
        # Set time to just before midnight for the end of the day
        formatted_end_date = datetime.combine(end_date, time.max).strftime('%Y-%m-%d %H:%M:%S')
    

        print("Parsed Begin Date:", begin_date)
        print("Parsed End Date:", end_date)
        print("Formatted Begin Date:", formatted_begin_date)
        print("Formatted End Date:", formatted_end_date)
       
        cursor.execute(query, (album_id, formatted_begin_date, formatted_end_date))
        photos = cursor.fetchall()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        cnx.close()
    return photos


def retrieve_thumbnails_by_album_id_within_date_range(album_id, begin_date_str, end_date_str, table_name = 'photos'):
    photos = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT id, album_id, source_name, date_taken, thumbnail_data
            FROM photos
            WHERE album_id = %s
            AND date_taken BETWEEN %s AND %s
            ORDER by date_taken DESC
        """.format(table_name)
         
        # Convert date strings to datetime.date objects
        begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Set time to midnight for the beginning of the day
        formatted_begin_date = datetime.combine(begin_date, time.min).strftime('%Y-%m-%d %H:%M:%S')
        # Set time to just before midnight for the end of the day
        formatted_end_date = datetime.combine(end_date, time.max).strftime('%Y-%m-%d %H:%M:%S')
    

        print("Parsed Begin Date:", begin_date)
        print("Parsed End Date:", end_date)
        print("Formatted Begin Date:", formatted_begin_date)
        print("Fformatted End Date:", formatted_end_date)
       
        cursor.execute(query, (album_id, formatted_begin_date, formatted_end_date))
        photos = cursor.fetchall()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        cnx.close()
    return photos


def retrieve_photo_by_id(photo_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT photo_data FROM photos WHERE id = %s"
        cursor.execute(query, (photo_id,))
        photo = cursor.fetchone()
        cursor.close()
        connection.close()
        return photo
    except mysql.connector.Error as err:
        print("Error retrieving photo:", err)
        return None

def retrieve_photos_by_album_id(album_id):
    photos = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT photo_data FROM photos WHERE album_id = %s ORDER by date_taken DESC"
        cursor.execute(query, (album_id,))
        photos = cursor.fetchall()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        cnx.close()
    return photos

def retrieve_latest_photo_for_album(album_id):
    try:
        print("--------Querying----------")
        print(album_id)
        photo = db.session.query(Photos.photo_data, Photos.date_taken).where(album_id == Photos.album_id).order_by(Photos.date_taken.desc()).first()
       # photo = cursor.fetchone()
    except Exception as err:
        print("-------MySQL Error:---------", err)
        photo = None
    return photo

def store_photo_in_database(photo_data, album_id, source_name, trigger_type, date_taken, photo_md5):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("------ STORING IN DATABASE --------")
        # Store the photo data and metadata in the database
        insert_query = """
        INSERT INTO photos (album_id, source_name, trigger_type, date_taken, photo_md5, photo_data, thumbnail_data, HD1080p_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Create a thumbnail from the photo_data
        photo = Image.open(io.BytesIO(photo_data))
        thumbnail = photo.copy()
        thumbnail.thumbnail(THUMBNAIL_SIZE)
        thumbnail_data = io.BytesIO()
        thumbnail.save(thumbnail_data, format='JPEG')


        # Create a 1080p version with horizontal width of 1088 pixels
  
        HD1080p = photo.resize((1648, 1088), Image.LANCZOS)
        HD1080p_data = io.BytesIO()
        HD1080p.save(HD1080p_data, format='JPEG')

        cursor.execute(insert_query, (album_id, source_name, trigger_type, date_taken, photo_md5, photo_data, thumbnail_data.getvalue(), HD1080p_data.getvalue()))
        connection.commit()

        cursor.close()
        connection.close()

        print("-------Photo stored in the database successfully---------")
     
    except mysql.connector.Error as err:
        print("Error storing photo in the database:", err)
        return jsonify({'status': 'Error', 'message': str(err)})


def retrieve_last_device_for_album(album_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = """
            SELECT device_id
            FROM photos
            WHERE album_id = %s
            ORDER BY date_taken DESC
            LIMIT 1
        """
        cursor.execute(query, (album_id,))
        result = cursor.fetchone()  # Fetch the tuple
        camera_id = result[0] if result else None  # Extract camera_id from the tuple
  
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        camera_id = None
    finally:
        cursor.close()
        cnx.close()
    return camera_id



def retrieve_photos_from_database(album_id=None):
    photos = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        
        if album_id is None:
            query = "SELECT id, album_id, source_name, date_taken, thumbnail_data FROM photos"
        else:
            query = "SELECT id, album_id, source_name, date_taken, thumbnail_data FROM photos WHERE album_id = %s"
            cursor.execute(query, (album_id,))
            
        photos = cursor.fetchall()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        cnx.close()
    return photos

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    try:
        albums = db.session.query(Photos.album_id).distinct()
        # db_connection = mysql.connector.connect(**db_config)
        # cursor = db_connection.cursor(dictionary=True)
        # query = "SELECT DISTINCT album_id FROM photos"
        # cursor.execute(query)
        # albums = cursor.fetchall()
        #db_connection.close()


    except Exception as err:
        print("MySQL Error:", err)
        albums = []
    print("---------albums----------")
    print(albums)
    today = datetime.now().date().strftime('%Y-%m-%d')  # Get today's date
    return render_template("index.html", albums=albums, today=today)


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/latest_photo/<int:album_id>', methods=['GET', 'POST'])
def latest_photo(album_id):

  

    photo = retrieve_latest_photo_for_album(album_id)
    date_taken = photo['date_taken']
    photo_filename = f'{album_id}_latest_photo_{date_taken}.jpg'
    filename = photo_filename.replace('/', '_').replace(' ','_').replace(':','_')
 
    print(filename)

    if request.method == 'GET':
       if photo:
            return Response(photo['photo_data'], content_type='image/jpeg', headers={'Content-Disposition': f'attachment; filename="{filename}"; download_name="{filename}"'})

       else:
            return "No photo found for the specified album ID", 404
  
    elif request.method == 'POST':
        if photo:
            return render_template('view_single_photo.html', photo=photo, from_latest_photo=True)
        else:
            return "No photo found for the specified album ID", 404

@app.route('/generate_timelapse/<int:album_id>', methods=['GET', 'POST'], strict_slashes=False)
def generate_timelapse(album_id):
    if request.method == 'POST':
        try:
            begin_date_str = request.form['begin_date']
            end_date_str = request.form['end_date']
            print("Begin Date:", begin_date_str)
            print("End Date:", end_date_str)
            

            
            # Retrieve photos from the specified album_id within the selected date range
            photos = retrieve_HD1080p_by_album_id_within_date_range(album_id, begin_date_str, end_date_str)
            print("Number of Photos:", len(photos))
            
            if not photos:
                return "No photos found in the selected date range."

            # Specify the output video path
            #video_path = f'generated/timelapse_video_{album_id}.mp4'
            video_path = f'generated/timelapse_video_{album_id}_{"".join(random.choices(string.ascii_letters + string.digits, k=8))}.mp4'

            # Specify the dimensions of the video frames (vertical resolution of 1080p)

            frame_width = 1920 #just to have it
            frame_height = 1088  # or 720 if you prefer /// 1088 because stupid encoder alignment need to be divisible by 16


# Find the first frame with HD1080p data to calculate the aspect ratio
            aspect_ratio_set = False
            for HD1080p_data in photos:
                if HD1080p_data.get('HD1080p_data'):
                    img_array = np.frombuffer(HD1080p_data['HD1080p_data'], dtype=np.uint8)
                    img = Image.open(BytesIO(img_array))
                    img_aspect_ratio = img.width / img.height
                    frame_width = int(frame_height * img_aspect_ratio)
                    aspect_ratio_set = True
                    break

            # Specify the desired frame rate for the timelapse video
            frame_rate = 30

           
 
            # out = cv2.VideoWriter(video_path, fourcc, frame_rate, (frame_width, frame_height))

            video_writer = imageio.get_writer(video_path, format='mp4', fps=frame_rate)

            # Iterate through the photos and add them to the video
            for HD1080p_data in photos:
                if HD1080p_data.get('HD1080p_data'):
                    try:
                        img_array = np.frombuffer(HD1080p_data['HD1080p_data'], dtype=np.uint8)
                        img = Image.open(BytesIO(img_array))

                        img_array_resized = np.array(img)
                        
                        video_writer.append_data(img_array_resized)
                    except Exception as e:
                        print("Error processing image:",e)
                        print("Image size:", img_array_resized.shape)
                        continue

            # Release the VideoWriter
            video_writer.close()

            generated_video_path = video_path
            generated_video_filename = os.path.basename(generated_video_path)
            print(generated_video_path)
            # Return the generated video directly to be played in the browser
            #return send_file(generated_video_path, as_attachment=False, mimetype='video/mp4')
            

            #for the template
            return render_template('generate_timelapse.html', generated_video_path=generated_video_path, generated_video_filename=generated_video_filename, album_id=album_id)


        except Exception as e:
            return f"Error generating timelapse: {e}"
    else:
        today = datetime.now().date().strftime('%Y-%m-%d')  # Get today's date
        
        # Render the HTML template
        return render_template('generate_timelapse.html', album_id=album_id, today=today)

@app.route('/get_generated_video/<path:video_filename>')
def get_generated_video(video_filename):
    print(video_filename)
    return send_from_directory('.', video_filename, as_attachment=True)

@app.route('/view_photos/<int:album_id>', methods=['GET', 'POST'], strict_slashes=False)
def view_photos(album_id):

    if request.method == 'POST':
        try:
            begin_date_str = request.form['begin_date']
            end_date_str = request.form['end_date']
            print("Begin Date:", begin_date_str)
            print("End Date:", end_date_str)

            # Retrieve photos from the specified album_id within the selected date range
            photos = retrieve_thumbnails_by_album_id_within_date_range(album_id, begin_date_str, end_date_str)
            print("Number of Photos:", len(photos))
            

            if not photos:
                return "No photos found in the selected date range."    

            return render_template('view_photos.html', photos=photos, album_id=album_id)
        
        except Exception as e:
            return f"Error generating photo view: {e}"

@app.route('/live_feed/<int:album_id>')
def live_feed(album_id):
    def generate_sse():
        global global_counter
        current_counter = None

        latest_photo_url = f"/latest_photo/{album_id}"  # Manually construct the URL
        sse.publish({"url": latest_photo_url}, type="latest_photo", channel=str(album_id))
        
        while True:
            ts.sleep(1)  # Adjust the interval for checking changes
            with lock:
                if current_counter != global_counter:
                    print("New SSE event")
                    latest_photo_url = f"/latest_photo/{album_id}"  # Manually construct the URL
                    sse.publish({"url": latest_photo_url}, type="latest_photo", channel=str(album_id))
                    current_counter = global_counter

    generate_sse()  # Just call the function to start SSE events
    return ""

@app.route('/camera_configurations')
def camera_configurations():
    try:
        cameras = db.session.query(Camera_Parameters)
        return render_template('camera_configuration.html', cameras=cameras)
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"

@app.route('/add_camera', methods=['GET', 'POST'])
def add_camera():
    if request.method == 'POST':
        camera_id = request.form.get('camera_id')
        source = request.form.get('source')
        album = request.form.get('album')
        timelapse = request.form.get('timelapse')

        try:
            # connection = mysql.connector.connect(**db_config)
            # cursor = connection.cursor()
            # insert_query = """
            # INSERT INTO camera_parameters (camera_id, source, album, timelapse)
            # VALUES (%s, %s, %s, %s)
            # """
            # cursor.execute(insert_query, (camera_id, source, album, timelapse))
            # connection.commit()
            # cursor.close()
            # connection.close()
            newParams = Camera_Parameters(
                id=id,
                camera_id=camera_id,
                source=source,
                album=album,
                timelapse=timelapse,
            )
            db.session.add(newParams)
            db.session.commit()
            
            return redirect(url_for('camera_configuration.html'))
        except mysql.connector.Error as err:
            return f"MySQL Error here: {err}"
    else:
        try:
            next_camera_id = db.session.query(func.max(Camera_Parameters.camera_id))
            return render_template('add_camera.html', next_camera_id=next_camera_id)
        except Exception as err:
            return f"MySQL Error: {err}"

@app.route('/edit_camera/<int:camera_id>', methods=['GET', 'POST'])
def edit_camera(camera_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM camera_parameters WHERE camera_id = %s"
        cursor.execute(query, (camera_id,))
        camera = cursor.fetchone()
        cursor.close()
        connection.close()
        if request.method == 'POST':
            source = request.form.get('source')
            album = request.form.get('album')
            timelapse = request.form.get('timelapse')

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            update_query = """
            UPDATE camera_parameters
            SET source = %s, album = %s, timelapse = %s
            WHERE camera_id = %s
            """
            cursor.execute(update_query, (source, album, timelapse, camera_id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
        else:
            return render_template('edit_camera.html', camera=camera)
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"

@app.route('/delete_camera/<int:camera_id>', methods=['POST'])
def delete_camera(camera_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        delete_query = "DELETE FROM camera_parameters WHERE camera_id = %s"
        cursor.execute(delete_query, (camera_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"


if __name__ == "__main__":
    app.run(debug=True)
