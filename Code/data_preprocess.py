from utils import mysql_connector
import pandas as pd

def read_fromDB():
    mydb, mycursor = mysql_connector()
    sql = "SELECT * FROM web_extraction.bookdata LIMIT 0, 379"
    mycursor.execute(sql)
    output = mycursor.fetchall()
    mydb.commit()
    df = pd.DataFrame (output, columns=['Id','Title','Rating','Price'])
    df.to_csv("Data_extracted_fromDB.csv",index=False)


def Preprocess():
    dfnd = pd.read_csv('Data_extracted_fromDB.csv')
    #Needed Columns
    dfnd1  = dfnd.loc[:,['Title','Rating','Price']]

    #Categorical Variable
    dfnd1['Rating'] = dfnd1['Rating'].replace({
        "One":1, "Two":2, "Three":3, "Four":4, "Five":5
    })

    #Drop Duplicates
    dfnd1.drop_duplicates(inplace=True)

    dfnd1.to_csv("Data_preprocess.csv",index=False)



    #Analytics
    #1. Total Number of Unique books
    print('Their are {} unique books'.format(len(dfnd1['Title'].value_counts())))

    #2. Top 5 Costlier books
    sorted_df = dfnd1.sort_values(by=['Price'], ascending=False)
    sorted_df1 = sorted_df.head()
    TopP = []
    for val in sorted_df1['Title']:
        TopP.append(val)
    print("These books are the costlier {} ".format(TopP))

    #3. Top 5 Low Price books
    sorted_df = dfnd1.sort_values(by=['Price'], ascending=True)
    sorted_df1 = sorted_df.head()
    LessP = []
    for val in sorted_df1['Title']:
        LessP.append(val)
    print("These books are the Low Price {} ".format(LessP))

    #4. Top 5 High Rated books
    sorted_df = dfnd1.sort_values(by=['Rating'], ascending=False)
    sorted_df1 = sorted_df.head()
    TopR = []
    for val in sorted_df1['Title']:
        TopR.append(val)
    print("These books are the High Rated books : {} ".format(TopR))

    #5. Top 5 Low Rated books
    sorted_df = dfnd1.sort_values(by=['Rating'], ascending=True)
    sorted_df1 = sorted_df.head()
    LowR = []
    for val in sorted_df1['Title']:
        LowR.append(val)
    print("These books are the Low Rated books : {} ".format(LowR))


    #6. High Rated Low Price books
    dfhr = dfnd1[dfnd1['Rating'] == 5]
    dfhrS = dfhr.sort_values(by=['Price'], ascending=True)
    for val in dfhrS['Title']:
        book_nd = val
        break
    print("Top Rated Low Price Books : {} ".format(book_nd))


    #7. Low Rated High Price books\
    dfhr = dfnd1[dfnd1['Rating'] == 1]
    dfhrS = dfhr.sort_values(by=['Price'], ascending=True)
    for val in dfhrS['Title']:
        book_nd = val
        break
    print("Low Rated High Price Books : {} ".format(book_nd))








if __name__ == "__main__":
    #read_fromDB()
    Preprocess()


