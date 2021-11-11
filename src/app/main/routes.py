from flask import Blueprint, render_template
from flask import url_for, redirect, request
from ..db_conf import mongo
from .change_detection.entry_point import image_change_detection
from bson.objectid import ObjectId
import gridfs
import numpy as np
from PIL import Image

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def tie_point():
    if request.method == 'POST':
        img = request.files['tie_point']
        mongo.save_file(img.filename, img)
        desc = request.form.get('tie_point_descricao')
        mongo.db.tie_point.insert({'descricao': desc, 'image_name': img.filename})
        return render_template('index.html')
    else:
        return render_template('index.html')


def get_tie_points_collection():
    return mongo.db.tie_point.find({})


def delete_tie_point_collection(file_id):
    query = {'_id': ObjectId(file_id)}
    mongo.db.tie_point.delete_one(query)
    return True

    
@main.route('/file/<filename>', methods=['GET'])
def file(filename):
    return mongo.send_file(filename)


@main.route('/tie_points', methods=['GET', 'POST'])
def get_all_tie_points():
    if request.method == 'POST':
        result = delete_tie_point_collection(request.values['tie_point_id'])
        return redirect(url_for('main.get_all_tie_points'))
    else:
        tie_ps = get_tie_points_collection()
        data = [{
            'descricao': tie_p.get('descricao'),
            'image_name': tie_p.get('image_name'),
            'file_path': f"{url_for('main.file', filename=tie_p['image_name'])}",
            'id': f"{tie_p.get('_id')}"
        } for tie_p in tie_ps]
        return render_template('tie_points_list.html', tie_points=data)


@main.route('/comparar', methods=['GET', 'POST'])
def comparar_imagens():
    if request.method == 'POST':
        source = Image.open(request.files['source'])
        source_array = np.array(source)

        template = Image.open(request.files['template'])
        template_array = np.array(template)

        tie_point_obj = mongo.db.tie_point.find_one({'_id': ObjectId(request.values['tie_point'])});
        imgn = tie_point_obj.get('image_name'); gfs = gridfs.GridFS(mongo.db).find_one({'filename': imgn})
        tie_point = Image.open(gfs)
        tie_point_array = np.array(tie_point)

        image_change_detection(source_array, template_array, tie_point_array)
        return redirect(url_for('main.resultado_comparacao'))

    tie_p = get_tie_points_collection()
    return render_template('comparar_imagens_form.html', tie_points=tie_p)


@main.route('/resultado_comparacao', methods=['GET'])
def resultado_comparacao():
    return render_template('resultado_comparacao_detail.html')