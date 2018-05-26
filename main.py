# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
import os
from google.appengine.ext import ndb

import pprint

import shopify
from flask import (
    Flask, Blueprint, render_template, current_app, request, redirect, session,
    url_for)

PROJECT = "Hello Shopify"
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TESTING = False

SECRET_KEY = 'secret key'

SERVER_NAME = "localhost:5000"
PREFERRED_URL_SCHEME = "https"

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/helloshopify.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

SHOPIFY_API_KEY = '###'
SHOPIFY_SHARED_SECRET = '###'

app = Flask(__name__)

class Shop(ndb.Model):
    shop = ndb.StringProperty()
    token = ndb.StringProperty()
    status = ndb.IntegerProperty()

@app.route('/')
@app.route('/index')
def home():
    # self.response.headers['Content-Type'] = 'text/plain'
    # self.response.write('hey!')
    return render_template('index.html')

@app.route('/install')
def install():
  
  shop_url = request.args.get("shop")
  
  shopify.Session.setup(
    api_key=SHOPIFY_API_KEY, 
    secret=SHOPIFY_SHARED_SECRET)
  
  session = shopify.Session(shop_url)
  
  scope=[
    "read_orders", "read_shipping", "read_script_tags", "write_script_tags",
    "read_marketing_events", "write_marketing_events", "read_content",
    "write_content","read_products", "write_products","read_customers",
    "read_analytics", "read_reports"]
  
  variable = "hi"
  # variable = url_for('install', _external=True)

  permission_url = session.create_permission_url(
    scope, "https://localhost:8080/finalize")
  
  return render_template(
    'install.html', permission_url=permission_url)


@app.route('/finalize')
def finalize():
  
  shop_url = request.args.get("shop")
  
  shopify.Session.setup(
      api_key=SHOPIFY_API_KEY, 
      secret=SHOPIFY_SHARED_SECRET)
  
  shopify_session = shopify.Session(shop_url)

  token = shopify_session.request_token(request.args)

  shop = Shop(shop=shop_url, token=token)
  # db.session.add(shop)
  # db.session.commit()

  session['shopify_url'] = shop_url
  session['shopify_token'] = token
  session['shopify_id'] = shop.id
  
  return redirect("https://localhost:8080/")