# AI-Load-Forecast (AI Powered Python Kong Plugin)
## Overview
Unlock the power of AI with our Kong plugin that predicts latency and request rates, enabling you to optimize service performance and enhance user experience in real time. By leveraging a Linear Regression model, our plugin turns historical log data into actionable insights, helping you proactively manage traffic and resources. Elevate your business with data-driven decisions and stay ahead of the competition.

## Tested in Kong Release
Kong Enterprise 3.4.3.11

## Installation
### Install Kong Pdk and Python Packages 
```
$ yum install && yum install python3 py3-pip python3-dev musl-dev libffi-dev gcc g++ file make && PYTHONWARNINGS=ignore pip3 install kong-pdk
$ pip install ipython numpy sklearn pandas jsons datetime
```
### Make the Below Changes in Kong.conf

```
$ pluginserver_names=python
$ pluginserver_python_socket=/usr/local/kong/python_pluginserver.sock
$ pluginserver_python_start_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> -v
$ pluginserver_python_query_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> --dump-all-plugins
```
After Installing the Plugin using any of the above steps . Add the Plugin Name in Kong.conf

```
plugins = bundled,AI-Load-Forecast

```
### Restart Kong

```
kong restart

```
# Configuration Reference

## Enable the plugin on a Route

### Admin-API
For example, configure this plugin on a service by making the following request:
		
curl -X POST http://{HOST}:8001/routes/{ROUTE}/plugins \
--data "name=AI-Load-Forecast"  \
--data "config.Log_File_Path={Log_File_Path}"

### Declarative(YAML)
For example, configure this plugin on a service by adding this section to your declarative configuration file:
			
	routes : 
	 name: {ROUTE}
	 plugins:
	 - name: AI-Load-Forecast
	 config:
	   Log_File_Path: {Log_File_Path}
	 enabled: true
	 protocols:
	 - grpc
	 - grpcs
	 - http
	 - https

ROUTE is the id or name of the route that this plugin configuration will target.
Log_File_Path is the Path of Log file.


## Parameters

| FORM PARAMETER      | DESCRIPTION |
| ----------- | ----------- |
| ROUTE Type:string      | The name of the Route  the plugin targets.       |
| config.Log_File_Path Type:string   | Log file path        |



## Contributors
Design & Developed By : Satyajit.Sial@VERIFONE.com ,preman1@verifone.com, dhavalm1@verifone.com
