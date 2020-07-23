from flask import Flask,jsonify
import urllib.request as request
import simplejson 
import json
import pymysql

app = Flask(__name__)

@app.route("/")
def home():
    name=[]
    ccode=[]
    capital=[]
    region=[]
    subregion=[]
    population=[]
    area=[]
    latlong=[]
    timezone=[]
    currency=[]
    flag=[]

    with request.urlopen('https://restcountries.eu/rest/v2') as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)
        else:
            print('An error occurred while attempting to retrieve data from the API.')
        for i in range(0,len(data)):
            name.append(data[i]['name'])
            ctemp=str(data[i]['callingCodes'][0])
            ccode.append(ctemp)
            capital.append(data[i]['capital'])
            region.append(data[i]['region'])
            subregion.append(data[i]['subregion'])
            population.append(data[i]['population'])
            if(str(data[i]['area'])=='None'):
                area.append(0)
            else:
                area.append(data[i]['area'])
            if(data[i]['latlng']==[]):
                latlong.append([0,0])
            else:    
                latlong.append(data[i]['latlng'])
            ttemp=(str(data[i]['timezones'][0]))
            timezone.append(ttemp)
            currency.append(data[i]['currencies'][0]['name'])
            flag.append(data[i]['flag'])

    # Connect to the database
    connection = pymysql.connect(host='sql12.freemysqlhosting.net',
                             user='sql12356306',
                             password='4lpG4FD3Za',
                             db='sql12356306')
    cursor = connection.cursor()
    # Create a new record
    for i in range(0,len(name)):
        sql = "INSERT INTO `country` (`name`, `code`, `capital`, `region`, `subregion`, `population`, `area`, `lat`, `lon`, `timezone`, `currency`, `flag`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name[i],ccode[i],capital[i],region[i],subregion[i],population[i],area[i],latlong[i][0],latlong[i][1],timezone[i],currency[i],flag[i]))
        connection.commit()

    cursor.execute("SELECT * FROM country")
    rows = cursor.fetchall()
    return jsonify(str(rows))


if __name__ == "__main__":
    app.run(debug = True)