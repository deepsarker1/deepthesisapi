#!/bin/bash

echo "Mariadb Started"

flask db migrate

flask db upgrade

flask run -h 0.0.0.0 -p 3005