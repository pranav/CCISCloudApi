#!/bin/bash

uwsgi -s 127.0.0.1:5000 -w cciscloud.web:app --enable-threads --protocol http
