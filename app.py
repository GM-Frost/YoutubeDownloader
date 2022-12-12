from flask import Flask, request, render_template, session, url_for, redirect, send_file
from pytube import YouTube
from io import BytesIO #it allows us to take video and stream into website. Like hosting into the application

app = Flask(__name__)
app.config['SECRET_KEY']=b'\xbb\x1c\x0fk\x92}\xc9\xb1`\x10\xb7\xd2`\x04\x06\xf8\xf6\x03\xdd"c\x1d\x99W'

@app.route('/',methods=["GET","POST"])
def home():
    errors = {}
    if request.method == 'POST':
        validation = request.form.get('youtubeURL')
        if validation == "":
            errors = ["URL cannot be Empty!"]
        else:
            session['link'] = request.form.get('youtubeURL')
            formatType = request.form.get('requestFormat')

            try:
                url = YouTube(session['link'])
                url.check_availability()

            except:

                return render_template('home.html', url="Invalid Link. Please try only with YouTube Links")

            if formatType == 'videoFormat':
                return render_template('downloadVideo.html',url=url)
            
            elif formatType == 'audioFormat':
                return render_template('downloadAudio.html',url=url)
            else:

                return render_template('home.html', url="Something went Wrong :(")
     
    return render_template('home.html', errors=errors)

@app.route("/downloadVideo",methods=["GET","POST"])
def downloadVideo():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag') #the resolution that user choose
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer) #allow video stream to buffer
        buffer.seek(0)
        fileName = url.streams[0].title

        return send_file(buffer, as_attachment=True, download_name=fileName+'.mp4',mimetype='video/mp4') #send the buffer to user
    return redirect(url_for('home')) #redirects the user to the home page if they dont click anything

@app.route("/downloadAudio",methods=["GET","POST"])
def downloadAudio():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag') #the resolution that user choose
        audio = url.streams.get_by_itag(itag)
        audio = url.streams.filter(only_audio=True).last()
        audio.stream_to_buffer(buffer) #allow video stream to buffer
        buffer.seek(0)
        fileName = url.streams[0].title

        return send_file(buffer, as_attachment=True, download_name=(fileName+'.mp3'),mimetype='.mp3 audio/mpeg') #send the buffer to user
    return redirect(url_for('home')) #redirects the user to the home page if they dont click anything

if __name__ == '__main__':
    app.run(debug=True)