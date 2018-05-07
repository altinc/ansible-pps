from flask import Flask, jsonify, request, Response
import xmlrpclib
import jinja2
import os
import urllib
import re

# Configuration Variables
global odoo_server
global odoo_user
global odoo_pass
global odoo_dbname

app = Flask(__name__)

def pps(mac, template):

    odoo_server = 'http://104.37.193.34:8069'
    odoo_user = 'admin'
    odoo_pass = 'admin'
    odoo_dbname = 'newdatabase'
    
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    user_agent = request.headers.get('User-Agent')
    
    username =  odoo_user #the user
    pwd =  odoo_pass    #the password of the user
    dbname =  odoo_dbname   #the database

    # Get the uid
    sock_common = xmlrpclib.ServerProxy (odoo_server + '/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)

    sock = xmlrpclib.ServerProxy(odoo_server + '/xmlrpc/object')
    d_args = [('x_unique', 'ilike', mac)] #query clause
    d_id = sock.execute(dbname, uid, pwd, 'kazoo_mgmt.devices', 'search', d_args)

    d_fields = ['x_unique','x_vlan','x_headset','x_model','x_partners','x_owner','x_site']
    d_data = sock.execute(dbname, uid, pwd, 'kazoo_mgmt.devices', 'read', d_id, d_fields) #i

    s_args = [('id', '=', d_data[0]['x_site'][0])] #query clause
    s_id = sock.execute(dbname, uid, pwd, 'kazoo_mgmt.sites', 'search', s_args)

    s_fields = ['x_gtz','x_city','x_co']
    s_data = sock.execute(dbname, uid, pwd, 'kazoo_mgmt.sites', 'read', s_id, s_fields) #i

    p_fields = ['firstname','x_voip_ext','x_voip_user','x_voip_secret','commercial_partner_id']
    p_data = sock.execute(dbname, uid, pwd, 'res.partner', 'read', sorted(d_data[0]['x_partners'], reverse=False), p_fields)

    o_fields_0 = ['name','ref','x_kazoo_realm','x_pbxip','x_kazoo_enabled', 'x_legacy']
    o_data_0 = sock.execute(dbname, uid, pwd, 'res.partner', 'read', p_data[0]['commercial_partner_id'][0], o_fields_0)

    user2 = True
    user3 = True
    user4 = True

    try:
        o_fields_1 = ['name','ref','x_kazoo_realm','x_pbxip','x_kazoo_enabled', 'x_legacy']
        o_data_1 = sock.execute(dbname, uid, pwd, 'res.partner', 'read', p_data[1]['commercial_partner_id'][0], o_fields_1)
    except:
        user2 = False
    
    try:
        o_fields_2 = ['name','ref','x_kazoo_realm','x_pbxip','x_kazoo_enabled', 'x_legacy']
        o_data_2 = sock.execute(dbname, uid, pwd, 'res.partner', 'read', p_data[2]['commercial_partner_id'][0], o_fields_2)
    except:
        user3 = False
    
    try:
        o_fields_3 = ['name','ref','x_kazoo_realm','x_pbxip','x_kazoo_enabled', 'x_legacy']
        o_data_3 = sock.execute(dbname, uid, pwd, 'res.partner', 'read', p_data[3]['commercial_partner_id'][0], o_fields_3)
    except:
        user4 = False
    
    srvtoggle = ""
    orgid = ""
    ext1 = ""
    display1 = ""
    username1 = ""
    password1 = ""
    ext2 = ""
    display2 = ""
    username2 = ""
    password2 = ""
    ext3 = ""
    display3 = ""
    username3 = ""
    password3  = ""
    ext4 = ""
    display4 = ""
    username4 = ""
    password4 = ""
    server1 = ""
    server2 = ""
    server3 = ""
    server4 = ""
    model = ""
    vlan = ""
    headset = ""
    tz = ""
    city = ""
    country = ""

    if o_data_0[0]['x_kazoo_enabled'] == bool(1):
        server1 = o_data_0[0]['x_kazoo_realm']
        srvtoggle1 = "1"
        srvtoggle = "1"
    else:
        server1 = o_data_0[0]['x_pbxip']
        srvtoggle1 = "0"
        srvtoggle = "0"
    
    if user2 == True:
        if o_data_1[0]['x_kazoo_enabled'] == bool(1):
            server2 = o_data_1[0]['x_kazoo_realm']
            srvtoggle2 = "1"
        else:
            server2 = o_data_1[0]['x_pbxip']
            srvtoggle2 = "0"

    if user3 == True:
        if o_data_2[0]['x_kazoo_enabled'] == bool(1):
            server3 = o_data_2[0]['x_kazoo_realm']
            srvtoggle3 = "1"
        else:
            server3 = o_data_2[0]['x_pbxip']
            srvtoggle3 = "0"

    if user4 == True:
        if o_data_3[0]['x_kazoo_enabled'] == bool(1):
            server4 = o_data_3[0]['x_kazoo_realm']
            srvtoggle4 = "1"
        else:
            server4 = o_data_3[0]['x_pbxip']
            srvtoggle4 = "0"

    # device settings
    try:
        orgid = o_data_0[0]['x_legacy']
        model = d_data[0]['x_model']
        vlan = d_data[0]['x_vlan']
        headset = d_data[0]['x_headset']
    except:
        orgid = ""
        model = ""
        vlan = ""
        headset = ""

    # site settings
    try:
        tz = s_data[0]['x_gtz']
        city = clean_name(s_data[0]['x_city'][1])
        if s_data[0]['x_co'][1] == "Canada" :
            country = "CA"
        else:
            country = "US"    
    except:
        tz = ""
        city = ""
        country = ""

    # account 1
    try:
        ext1 = p_data[0]['x_voip_ext']
        display1 = p_data[0]['x_voip_ext'] + " : " + p_data[0]['firstname']
        username1 = p_data[0]['x_voip_user']
        password1 = p_data[0]['x_voip_secret']
    except:
        ext1 = ""
        display1 = ""
        username1 = ""
        password1 = ""

    # account 2
    try:
        ext2 = p_data[1]['x_voip_ext']
        display2 = p_data[1]['x_voip_ext'] + " : " + p_data[1]['firstname']
        username2 = p_data[1]['x_voip_user']
        password2 = p_data[1]['x_voip_secret']
    except:
        ext2 = ""
        display2 = ""
        username2 = ""
        password2 = ""
    # account 3
    try:
        ext3 = p_data[2]['x_voip_ext']
        display3 = p_data[2]['x_voip_ext'] + " : " + p_data[2]['firstname']
        username3 = p_data[2]['x_voip_user']
        password3  = p_data[2]['x_voip_secret']

    except:
        ext3 = ""
        display3 = ""
        username3 = ""
        password3  = ""

    # account 4
    try:
        ext4 = p_data[3]['x_voip_ext']
        display4 = p_data[3]['x_voip_ext'] + " : " + p_data[3]['firstname']
        username4 = p_data[3]['x_voip_user']
        password4 = p_data[3]['x_voip_secret']
    except:
        ext4 = ""
        display4 = ""
        username4 = ""
        password4 = ""

    templateVars = {
            "mac" : mac,
            "srvtoggle" : srvtoggle,
            "orgid" : orgid,
            "ext1" : ext1,
            "display1" : display1,
            "username1" : username1,
            "password1" : password1,
            "ext2" : ext2,
            "display2" : display2,
            "username2" : username2,
            "password2" : password2,
            "ext3" : ext3,
            "display3" : display3,
            "username3" : username3,
            "password3 " : password3,
            "ext4" : ext4,
            "display4" : display4,
            "username4" : username4,
            "password4" : password4,
            "server1" : server1,
            "server2" : server2,
            "server3" : server3,
            "server4" : server4,
            "model" : model,
            "vlan" : vlan,
            "headset" : headset,
            "tz" : tz,
            "city" : city,
            "country" : country
        }
    outputText = template.render( templateVars )
    return outputText
    
@app.route("/pc/<macxml>")
def pps_pc(macxml):

    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    user_agent = request.headers.get('User-Agent')

    TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2130.xml')

    if "GXP2130" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2130.xml')

    if "GXP2135" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2135.xml')

    if "DP715" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'DP715.xml')

    template = templateEnv.get_template( TEMPLATE_FILE )

    a,b = macxml.split(".")
    c,mac = a.split("g")
    
    return Response(pps(mac, template), mimetype='text/xml; charset=utf-8')

@app.route("/gs/<macxml>")
def pps_gs(macxml):

    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    user_agent = request.headers.get('User-Agent')

    TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2130.xml')

    if "GXP2130" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2130.xml')

    if "GXP2135" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'GXP2135.xml')

    if "DP715" in user_agent:
        TEMPLATE_FILE = os.path.join(app.root_path, 'templates', 'DP715.xml')

    template = templateEnv.get_template( TEMPLATE_FILE )

    a,b = macxml.split(".")
    c,mac = a.split("g")
    
    return Response(pps(mac, template), mimetype='text/xml; charset=utf-8')


def clean_name(s):

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"\'", '', s)

     return s

@app.route("/health")
def health():
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
