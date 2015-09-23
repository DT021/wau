import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask.ext.mail import Mail, Message
from flask.ext.sqlalchemy import SQLAlchemy
# from celery import Celery
from app import db, app, celery

from models import MapInfo
from crawl_naver import crawl
from models import GeoInfo
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@celery.task
def request_async_crawl(index_from, crawl_size):
    result_list = crawl(index_from, crawl_size)
    for each_result in result_list:
        geo_info = each_result
        cate_group = re.match('(.*)(>)(.*)',geo_info['category'])
        try:
            if cate_group is None:
                category1 = None
                category2 = None
            else:
                category1 = cate_group.group(1)
                category2 = cate_group.group(3)

            if GeoInfo.query.filter_by(latitude=geo_info['y'], longitude=geo_info['x'], name=geo_info['name']).first() is not None:
                pass
            else:
                geoInfo = GeoInfo(
                    latitude=geo_info['y'], 
                    longitude=geo_info['x'],
                    name=geo_info['name'],
                    address=geo_info['address'],
                    roadAddr = geo_info['roadAddr']['text'],
                    description = geo_info['description'],
                    phone = geo_info['phone'],
                    homepage = geo_info['landingHomepage'],
                    subwayID = geo_info['subwayId'],
                    category1 = category1,
                    category2 = category2 )
                db.session.add(geoInfo)
                db.session.commit()
                db.session.flush()
        except Exception as e:
            print e



@celery.task(bind=True)
def request_crawl(self):
    result_list = crawl(0, 10)
    print 'hi'
    for each_result in result_list:
        
        self.update_state(state='PROGRESS',
                          meta={'current': each_result, 'total': 'total',
                                'status': each_result})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        geoInfo = []
        try:
            geoInfo = GeoInfo.query.order_by(GeoInfo.category1.desc(), GeoInfo.category2.desc()).all()
            size = len(geoInfo)
        except Exception as e:
            print e
        return render_template('crawl.html', size=size,  geoInfo=geoInfo, index_from=session.get('index_from', 0), crawl_size=session.get('crawl_size',0))
    index_from = int(request.form['index_from'])
    crawl_size = int(request.form['crawl_size'])
    session['index_from'] = index_from
    session['crawl_size'] = crawl_size
    # send the email
    # task = request_crawl.apply_async()
    # print task.get(timeout=1)
    divided_size = crawl_size/3
    task = request_async_crawl.delay(index_from, divided_size)
    task = request_async_crawl.delay(index_from+divided_size, divided_size)
    task = request_async_crawl.delay(index_from+divided_size*2, divided_size)
    # if request.form['submit'] == 'Send':
    #     # send right away
    #     request_async_crawl.delay(msg)
    #     flash('Sending email to {0}'.format(email))
    # else:
    #     # send in one minute
    #     send_async_email.apply_async(args=[msg], countdown=60)
    #     flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
