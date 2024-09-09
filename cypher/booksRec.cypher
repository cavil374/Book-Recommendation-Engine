MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;


order: 

LOAD CSV WITH HEADERS FROM 'file:///split1Clean.csv' AS row
CREATE (b:Book {
    ISBN: toInteger(row.ISBN),
    Book_Title: row.Book_Title,
    Year_Of_Publication: toInteger(row.Year_Of_Publication),
    Publisher: row.Publisher,
    Image_URL_S: row.Image_URL_S,
    Image_URL_M: row.Image_URL_M,
    Image_URL_L: row.Image_URL_L
})

MERGE (a:Author {Name: row.Book_Author})
MERGE (a)-[:WROTE]->(b);

LOAD CSV WITH HEADERS FROM 'file:///auraUsers.csv' AS row
MERGE (u:User {User_ID: row.User_ID})
WITH u, row
MATCH (b:Book {ISBN: toInteger(row.ISBN)})
CREATE (u)-[:RATED {Book_Rating: toInteger(row.Book_Rating), ISBN: row.ISBN}]->(b);

LOAD CSV WITH HEADERS FROM 'file:///genresList.csv' AS row
UNWIND [row.Genre, row.Genre1, row.Genre2, row.Genre3] AS genreName
WITH genreName, row
WHERE genreName IS NOT NULL AND genreName <> ''
MERGE (g:Genre {name: genreName})
WITH g, row
MATCH (b:Book {ISBN: toInteger(row.ISBN)})
CREATE (b)-[:HAS_GENRE]->(g);


LOAD CSV WITH HEADERS FROM 'file:///criticRecs.csv' AS row
CREATE (c: Critic {Critic_ID: row.Critic_ID})
WITH c, row
MATCH (b:Book {ISBN: row.ISBN})
CREATE (c)-[:REVIEWED {Review_ID: row.Review_ID, ISBN: row.ISBN, Recommendation: row.Recommend}]->(b);

////



MATCH (n) DETACH DELETE n

MATCH (u1:User)-[:RATED]->(book1)
WITH u1, collect(book1.ISBN) AS u1Books
MATCH (u2:User)-[:RATED]->(book2) 
WHERE u1 <> u2
WITH u1, u1Books, u2, collect(book2.ISBN) AS u2Books
RETURN u1.User_ID AS User1, u2.User_ID AS User2,
       gds.similarity.jaccard(u1Books, u2Books) AS jaccard
ORDER BY jaccard DESC
LIMIT 10;


MATCH (u1:User {User_ID: '345737'})-[:RATED]->(book1)
WITH u1, collect(id(book1)) AS u1Books
MATCH (u2:User)-[:RATED]->(book2) WHERE u1 <> u2
WITH u1, u1Books, u2, collect(id(book2)) AS u2Books
RETURN u1.User_ID AS from, u2.User_ID AS to,
   gds.similarity.jaccard(u1Books, u2Books) AS jaccard;

MATCH (u1:User {User_ID: '100012'})-[:RATED]->(book1)
WITH u1, collect(id(book1)) AS u1Books
MATCH (u2:User)-[:RATED]->(book2) WHERE u1 <> u2
WITH u1, u1Books, u2, collect(id(book2)) AS u2Books
RETURN u1.User_ID AS User1, u2.User_ID AS User2,
   gds.similarity.jaccard(u1Books, u2Books) AS jaccard ORDER BY jaccard DESC;

// actual VVVV
MATCH (u1:User)-[:RATED]->(book1)
WITH u1, collect(book1.ISBN) AS u1Books
MATCH (u2:User)-[:RATED]->(book2) 
WHERE u1 <> u2
WITH u1, u1Books, u2, collect(book2.ISBN) AS u2Books
RETURN u1.User_ID AS User1, u2.User_ID AS User2,
       gds.similarity.jaccard(u1Books, u2Books) AS jaccard
ORDER BY jaccard DESC
LIMIT 10;

// actual ^^^^^

MATCH (u1:User {User_ID: '100121'})-[r1:RATED]->(b:Book)<-[r2:RATED]-(u2:User)
WHERE u1 <> u2 AND u2.User_ID = {otherUserId}
RETURN b.Book_Title AS Title, b.ISBN AS ISBN, COLLECT(u1.User_ID) AS UsersRated



MATCH (u:User {User_ID: '100121'})-[r:RATED]->(b:Book)-[:HAS_GENRE]->(g:Genre)
RETURN b.Book_Title AS Title, b.ISBN AS ISBN, r.Book_Rating AS Rating, COLLECT(g.name) AS Genres
ORDER BY r.Book_Rating DESC

MATCH (u:User {User_ID: '100121'})-[r:RATED]->(b:Book)-[:HAS_GENRE]->(g:Genre)
RETURN g.name AS Genre, COUNT(g) AS GenreCount
ORDER BY GenreCount DESC



//LOAD CSV WITH HEADERS FROM 'file:///genres.csv' AS row
//MERGE (g: Genre {name: row.Genre})
//WITH g,row
//MATCH (b:Book {ISBN: row.ISBN})
//CREATE (b)-[:HAS_GENRE]->(g);