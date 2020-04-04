from mary.mctourdb.model import project

sql_create_reviews_table = """ CREATE TABLE IF NOT EXISTS reviews (
                                        id integer PRIMARY KEY,
                                        author text NOT NULL,
                                        project_id text NOT NULL,
                                        rating integer NOT NULL,
                                        description text
                                    ); """



def select_reviews_by_project(conn,project_id):
    """
        Query tasks by priority
        :param conn: the Connection object
        :param author:
        :param project_id
        :return: Project
        """
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE project_id=?", (project_id,))

    rows = cur.fetchall()
    reviews = []
    for row in rows:
        reviews.append(Review(*row))
    return reviews

def select_review_by_author_and_project(conn,author,project_id):
    """
        Query tasks by priority
        :param conn: the Connection object
        :param author:
        :param project_id
        :return: Project
        """
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE author=? and project_id=?", (author,project_id))

    rows = cur.fetchall()
    if len(rows) == 1:
        return Review(*(rows[0]))
    else:
        return None


class Review:
    def __init__(self, id, author, project_id, rating, description):
        self.id = id
        self.author = author
        self.project_id = project_id
        self.rating = rating
        self.description = description

    def save_review(self, conn):
        """
        Create a new project into the projects table
        :param conn:
        """
        r = select_review_by_author_and_project(conn,self.author,self.project_id)
        if r is None:
            p = project.select_project_by_name(conn,self.project_id)
            if p is not None:
                sql = ''' INSERT INTO reviews(author,project_id,rating,description)
                          VALUES(?,?,?,?) '''
                with conn:
                    print('here')
                    cur = conn.cursor()
                    cur.execute(sql, (self.author, self.project_id, self.rating, self.description))
                return "Saved new review"
            else:
                return "Project doesn't exist"
        else:
            sql = ''' UPDATE reviews
                                      SET 
                                          rating = ? ,
                                          description = ?
                                      WHERE author = ? and project_id = ?'''
            with conn:
                cur = conn.cursor()
                cur.execute(sql, (self.rating, self.description, self.author, self.project_id))
                conn.commit()
            return "Updated review"

    def __str__(self) -> str:
        return """
Review
Author: {0}
Rating: {1}/10
description: {2}
    """.format(self.author, self.rating, self.description)

    def __repr__(self) -> str:
        return self.__str__()