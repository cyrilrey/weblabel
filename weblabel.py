#!/usr/bin/python

#import
import os #global
from StringIO import StringIO #some kind of temp file storage
from flask import (  #web framework
    Flask,
    render_template,
    send_from_directory,
    send_file,
    request,
    redirect,
    url_for,
    request,
    session,
    Response,
)
from escpos.printer import Usb #printer driver
from cairosvg import svg2png    #svg to bitmap

# create flask app
app = Flask(__name__)
app.secret_key = '4334fdsergsFGSDfsdfgSgfdsgsdsresgdsSERE'.encode('utf8')


# return css static files
@app.route('/Semantic-UI-CSS/<path:path>')
def send_js(path):
    return send_from_directory('Semantic-UI-CSS', path)

# return a label svg template from collection 
@app.route('/svgtemplate/<path:path>')
def send_label(path):
    return send_from_directory('templates/labels', path)


# index page
@app.route('/')
def do_index():
   return redirect(url_for('do_choose')) #redirect to choose


# choose page
@app.route('/choose')
def do_choose():
    labels = os.listdir('templates/labels') #read all files
    return render_template('choose.html', labels = labels)

# select page
@app.route('/edit', methods=['GET'])
def do_edit():
    
    try:
        session['labelsvg'] = request.args['labelsvg']
    except Exception as e:
        if session['labelsvg'] == "":
            return(str(e))
    
    return render_template('edit.html')

# preview page
@app.route('/preview', methods=['POST'])
def do_preview():

    session['txt1'] = request.form['txt1']
    session['txt2'] = request.form['txt2']
    session['txt3'] = request.form['txt3']
    session['txt4'] = request.form['txt4']

    return render_template('edit.html')




# return svg image
@app.route('/prev_img_svg')
def send_preview_img():
	#label template engine
	session['svglabel'] = render_template("labels/"+session['labelsvg'],txt1 =session['txt1'], txt2 =session['txt2'],txt3 =session['txt3'],txt4 =session['txt4'],)
	return Response(session['svglabel'],mimetype='image/svg+xml')

	
#print image
@app.route('/print')
def do_print():
   
    #config printer
    p = Usb(0x4b43, 0x3538,0 ,0xB2, 0x02  )
    #   lsus
    #   lsusb -vvv -d 4b43:3538"b
    #   sudo usermod -a -G dialout user
    #   sudo usermod -a -G tty user
    #   sudo usermod -a -G lp user
    #   ls -la /dev/usb/


    pngfile = StringIO() #temp file
    pngbuffer = svg2png(bytestring=session['svglabel'].decode('utf-8').encode('ascii'), dpi=171, write_to=pngfile) #SVG to PNG

    # image = 384 x 175  -- print area =  384 x 154 
    p.image(pngfile) #PNG to printer

    return render_template('edit.html')

