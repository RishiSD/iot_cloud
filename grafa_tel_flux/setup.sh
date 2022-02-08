#!/usr/bin/bash

mkdir /etc/mosquitto/
mkdir /etc/telegraf/
mkdir /etc/influxdb/

cp .mosquitto.env /etc/mosquitto/.mosquitto.env
cp .influxdb.env /etc/influxdb/.influxdb.env
cp .telegraf.env /etc/telegraf/.telegraf.env
cp telegraf.conf /etc/telegraf/telegraf.conf
