from bs4 import BeautifulSoup
import requests
import re
import sqlite3 

def createdb():
    con = sqlite3.connect('Imdb_movies.db')
    cur = con.cursor()
    try:
        cur.execute("DROP TABLE tamilmovie")     
    except:
        pass
    
    # CREATE TABLE IF NOT EXISTS tamilmovie
    query = """CREATE TABLE  tamilmovie(
            Rank INTEGER Primary key,     Name TEXT,    Year TEXT,
            Cert TEXT,        time TEXT,    Gene TEXT,
            Rate INTEGER,     Desc TEXT,    dir  TEXT,
            star TEXT,        img  TEXT
            )
        """
    cur.execute(query)
    con.commit()
    print('Imdb_movies Database & New Table tamilmovie Created Successfully ')
createdb()
  
entry = 'true'

try:
    url         = 'https://www.imdb.com/list/ls073097522/'
    response    = requests.get(url )
    soup        = BeautifulSoup(response.text,'html.parser')        # html code extracted
    tamilmovies = soup.find('div',class_='lister-list').find_all('div',class_='lister-item mode-detail')

    for movie in tamilmovies:

        # Extract Images 
        img_url   = movie.find('div',class_='lister-item-image ribbonize').find('img')['loadlate']
        img_res   = requests.get(img_url)
        movie_img = img_res.content

        #Extract Rank
        movie_rank = movie.find('div',class_='lister-item-content').find('span',class_='lister-item-index unbold text-primary').text
        movie_rank = movie_rank.split('.')[0] 
        
        # Extract Name
        movie_name = movie.find('div',class_='lister-item-content').a.text  
        
        # Extract Year
        movie_year = movie.find('div',class_='lister-item-content').find('span',class_='lister-item-year text-muted unbold').text
        movie_year = re.sub(r'[()]', '', movie_year)
        
        # Extract Certification
        try:
            movie_cert = movie.find('p',class_='text-muted text-small').find('span',class_='certificate').text
        except:
            movie_cert = 'Not rated'

        # Extract Run time
        try:
            movie_time = movie.find('p',class_='text-muted text-small').find('span',class_='runtime').text
        except:
            movie_time = ' '
        
        # extract Generic Details
        try:
            movie_gen  = movie.find('p',class_='text-muted text-small').find('span',class_='genre').text
            movie_gen  = movie_gen.strip()
        except:
            movie_gen = ' '
        
        # extract Rating
        movie_rate = movie.find('div',class_='ipl-rating-widget').find('span',class_="ipl-rating-star__rating").text
        
        # Extract Description
        movie_des  = movie.find('div',class_='lister-item-content').find_all('p')
        movie_des  = movie_des[1].text
        movie_des  = movie_des.strip()

        # Extract Diretcor Details
        movie_dir  = movie.find('p',class_='text-muted text-small').findNext('p',class_='text-muted text-small').a.text
        
        # Extract Stars
        movie_star = movie.find('p',class_='text-muted text-small').findNext('p',class_='text-muted text-small').find_all('a')
        movie_star = movie_star[1:len(movie_star)]
        mstar = []
        for i in movie_star:
            mstar.append(i.text)
        star = ' '.join(mstar)

     
        #print(img_url,movie_rank,' ',movie_name,' ',movie_year,' ',movie_cert,' ',movie_time,' ',movie_gen,' ' , movie_rate,' ',movie_dir,' ',star)
               
        # Store in Data Base
        con = sqlite3.connect('Imdb_movies.db')
        cur = con.cursor()
        qry = """INSERT INTO tamilmovie (Rank,Name,Year,Cert,time,Gene,Rate,Desc,dir,star,img) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
        new_value = (movie_rank,movie_name,movie_year,movie_cert,movie_time,movie_gen,movie_rate,movie_des,movie_dir,star,img_url)
        cur.execute(qry,new_value)
        con.commit()





except Exception as msg:
    print('Error Msg : ',msg)
    entry = 'false'

con.close()



if entry =='true':
    print('Tamilmovies succesfully stored in IMDB database')

else: 
    print('Error in saving Data')
    

