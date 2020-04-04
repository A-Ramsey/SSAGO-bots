sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        name text PRIMARY KEY,
                                        warp text,
                                        map_url text,
                                        description text
                                    ); """

def get_random_project(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects ORDER BY RANDOM() LIMIT 1;")
    rows = cur.fetchall()
    if len(rows) == 1:
        return Project(*(rows[0]))
    else:
        return None

def select_project_by_name(conn, name):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param name:
    :return: Project
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE name=?", (name,))

    rows = cur.fetchall()
    if len(rows) == 1:
        return Project(*(rows[0]))
    else:
        return None

def select_all_projects(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")

    rows = cur.fetchall()
    projects = []
    for row in rows:
        projects.append(Project(*row))
    return projects


class Project:
    def __init__(self, name, warp, mapURL, description):
        self.name = name
        self.warp = warp
        self.mapURL = mapURL
        self.description = description

    def save_project(self, conn):
        """
        Create a new project into the projects table
        :param conn:
        """
        p = select_project_by_name(conn,self.name)
        if p is None:
            sql = ''' INSERT INTO projects(name,warp,map_url,description)
                  VALUES(?,?,?,?) '''
            with conn:
                cur = conn.cursor()
                cur.execute(sql, (self.name, self.warp, self.mapURL, self.description))
            return "Saved new project"
        else:
            sql = ''' UPDATE projects
                              SET 
                                  warp = ? ,
                                  map_url = ?,
                                  description = ?
                              WHERE name = ?'''
            with conn:
                cur = conn.cursor()
                cur.execute(sql, (self.warp, self.mapURL, self.description,self.name))
                conn.commit()
            return "Updated project"

    def __str__(self) -> str:
        return """
Project
Name: {0}
warp: `/warp {1}`
mapUrl: {2}
description: {3}
""".format(self.name,self.warp,self.mapURL,self.description)

    def __repr__(self) -> str:
        return self.__str__()


