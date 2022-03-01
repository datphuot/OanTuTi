from flask import *
from random import *
import os
from pathlib import Path
import json
import pickle
import datetime
app = Flask(__name__)
app.secret_key = '123456'


#url_for('data', filename='random_id.txt')
@app.route('/')
#màn hình start
def welcome():
    mixchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_id = "".join(choice(mixchars) for x in range(randint(10, 20)))
    return render_template('start.html', random_id=random_id)


#màn hình chơi game
@app.route('/play/<random_id>')
def play(random_id):
    my_file = Path("static/data/"+random_id+".txt")
    if my_file.is_file():

        file = open("static/data/" + random_id + ".txt",'rb')
        data_json = pickle.load(file, encoding='latin1')
        file.close()


        cookie_name = "admin_" + str(random_id)
        if request.cookies.get(cookie_name):
            admin = 1
        else:
            admin = 0

        return render_template('play.html', random_id=random_id, admin=admin, data_json=data_json)
    else:
        mixchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        cookie_name = "admin_" + str(random_id)
        cookie_value = "".join(choice(mixchars) for x in range(randint(10, 20)))

        admin = 1
        data_json = {
            'cookie_admin': cookie_value
        }
        resp = make_response(render_template('play.html', random_id=random_id, data_json=data_json, admin=admin))

        resp.set_cookie(cookie_name, cookie_value,max_age = 60 * 60 * 24 * 30)

        file = open("static/data/" + random_id + ".txt", 'wb')
        pickle.dump(data_json,file)
        file.close()


        return resp

#action chơi game

@app.route('/action/<random_id>', methods=['GET', 'POST'])
def active1(random_id):
    my_file = Path("static/data/" + random_id + ".txt")
    if my_file.is_file():

        file = open("static/data/" + random_id + ".txt", 'rb')
        data_json = pickle.load(file, encoding='latin1')
        file.close()

        cookie_name = "admin_" + str(random_id)
        if request.cookies.get(cookie_name):
            key_to_lookup = 'user_choi'
            if key_to_lookup in data_json:
                data_json['admin_choi'] = request.args.get('choose')

                if 'ti_so' not in data_json:
                    data_json['ti_so'] = {
                        'vong': 0,
                        'admin_thang': 0,
                        'admin_thua': 0,
                        'hoa': 0,
                        'user_thang': 0,
                        'user_thua': 0,
                    }
                #Kết quả hòa
                if data_json['admin_choi'] == data_json['user_choi']:
                    data_json['ket_qua'] = 'hoa'
                    data_json['ti_so']['hoa'] = data_json['ti_so']['hoa'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1
                elif data_json['admin_choi'] == 'keo' and data_json['user_choi']=='xoe':

                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['admin_thang'] = data_json['ti_so']['admin_thang']+1
                    data_json['ti_so']['user_thua'] = data_json['ti_so']['user_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'xoe' and data_json['user_choi']=='keo':
                    data_json['ket_qua'] = 'thua'
                    data_json['ti_so']['admin_thua'] = data_json['ti_so']['admin_thua']+1
                    data_json['ti_so']['user_thang'] = data_json['ti_so']['user_thang'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'keo' and data_json['user_choi']=='bua':
                    data_json['ket_qua'] = 'thua'
                    data_json['ti_so']['admin_thua'] = data_json['ti_so']['admin_thua']+1
                    data_json['ti_so']['user_thang'] = data_json['ti_so']['user_thang'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'bua' and data_json['user_choi']=='keo':
                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['admin_thang'] = data_json['ti_so']['admin_thang']+1
                    data_json['ti_so']['user_thua'] = data_json['ti_so']['user_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'bua' and data_json['user_choi']=='xoe':
                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['admin_thang'] = data_json['ti_so']['admin_thang']+1
                    data_json['ti_so']['user_thua'] = data_json['ti_so']['user_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1
                else:
                    pass

                # xóa phiên cũ
                del data_json['user_choi']
                del data_json['admin_choi']
            else:
                data_json['admin_choi'] = request.args.get('choose')
                if 'ti_so' not in data_json:
                    data_json['ti_so'] = {
                        'vong': 1,
                        'admin_thang': 0,
                        'admin_thua': 0,
                        'hoa': 0,
                        'user_thang': 0,
                        'user_thua': 0,
                    }
                if 'ket_qua' in data_json:
                    del data_json['ket_qua']

            file = open("static/data/" + random_id + ".txt", 'wb')
            pickle.dump(data_json, file)
            file.close()

            return data_json
        else:
            key_to_lookup = 'admin_choi'
            if key_to_lookup in data_json:
                data_json['user_choi'] = request.args.get('choose')
                if 'ti_so' not in data_json:
                    data_json['ti_so'] = {
                        'vong': 0,
                        'admin_thang': 0,
                        'admin_thua': 0,
                        'hoa': 0,
                        'user_thang': 0,
                        'user_thua': 0,
                    }

                if data_json['admin_choi'] == data_json['user_choi']:
                    data_json['ket_qua'] = 'hoa'
                    data_json['ti_so']['hoa'] = data_json['ti_so']['hoa']+1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'keo' and data_json['user_choi'] == 'xoe':

                    data_json['ket_qua'] = 'thua'
                    data_json['ti_so']['user_thua'] = data_json['ti_so']['user_thua']+1
                    data_json['ti_so']['admin_thang'] = data_json['ti_so']['admin_thang'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'xoe' and data_json['user_choi'] == 'keo':
                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['user_thang'] = data_json['ti_so']['user_thang']+1
                    data_json['ti_so']['admin_thua'] = data_json['ti_so']['admin_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1


                elif data_json['admin_choi'] == 'keo' and data_json['user_choi'] == 'bua':
                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['user_thang'] = data_json['ti_so']['user_thang']+1
                    data_json['ti_so']['admin_thua'] = data_json['ti_so']['admin_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'bua' and data_json['user_choi'] == 'xoe':
                    data_json['ket_qua'] = 'thang'
                    data_json['ti_so']['user_thang'] = data_json['ti_so']['user_thang']+1
                    data_json['ti_so']['admin_thua'] = data_json['ti_so']['admin_thua'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1

                elif data_json['admin_choi'] == 'bua' and data_json['user_choi'] == 'keo':
                    data_json['ket_qua'] = 'thua'
                    data_json['ti_so']['user_thua'] = data_json['ti_so']['user_thua']+1
                    data_json['ti_so']['admin_thang'] = data_json['ti_so']['admin_thang'] + 1
                    data_json['ti_so']['vong'] = data_json['ti_so']['vong'] + 1
                else:
                    pass

                #xóa phiên cũ
                del data_json['user_choi']
                del data_json['admin_choi']
            else:
                data_json['user_choi'] = request.args.get('choose')

                if 'ti_so' not in data_json:
                    data_json['ti_so'] = {
                        'vong': 1,
                        'admin_thang': 0,
                        'admin_thua': 0,
                        'hoa': 0,
                        'user_thang': 0,
                        'user_thua': 0,
                    }
                if 'ket_qua' in data_json:
                    del data_json['ket_qua']

            file = open("static/data/" + random_id + ".txt", 'wb')
            pickle.dump(data_json, file)
            file.close()

            return data_json

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
