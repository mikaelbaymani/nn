#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True


import nn
from flask import Flask,Response,request,stream_with_context


APP = Flask( __name__ )
DEFAULT = { 'fname' : '1', 'topk' : '10', 'truncate' : '80' }
HTMLENCODE = lambda s: s.replace('\n', '<br>').replace(' ', '&nbsp;')


@APP.route( '/', methods = ['GET', 'POST'] )
def index( ):

    if request.method == 'POST' :

        @stream_with_context
        def post():
            data = { key:value for key, value in request.form.items() }
            data.update( { key:DEFAULT[key] for key, value in data.items() if not value } )


            yield '''
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <style>
              code {
                font-family:courier, monospace;
                font-size:12px;
                border:0px solid #000000;}
            </style>'''
            try:
                yield '''
            <code><p>''' + HTMLENCODE( nn.query( data['fname'], 'key', data['topk'], data['truncate'] ).to_string() ) + '''
            </p></code>'''
            except Exception as e:
                yield '''
            <code><p>''' + HTMLENCODE( str(e) ) + '''
            </p></code>'''
            finally:
                yield '''
            <form>
              <input type="button" value="BACK" onclick="history.back()">
            </form>'''


        return Response( post(), mimetype='text/html' )


    if request.method == 'GET' :

        def get():


            yield '''
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <script>
            $(document).ready(function() {
              $('.advanced').click(function() {
                $('#hide').toggleClass("hidden");
              });
            });
            </script>
            <style>
            .hidden {
              display:none;
            }
            </style>
            <form method="POST" onsubmit="FromSubmit(this);">
              <input type="text" id="fname" name="fname" value="">
              <select name="topk">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
                <option value="200">200</option>
              </select>
              <label class="advanced"> + </label>
              <label id="hide" class="hidden">
                <input type="text" id="truncate" name="truncate" value="" size="3">
              </label><br><br>
              <input type="submit" value="NNS" />
            </form>'''


        return Response( get(), mimetype='text/html' )


if __name__ == "__main__" :

    APP.run()

# eof
