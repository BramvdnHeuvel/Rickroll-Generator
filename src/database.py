import sqlite3, random

def visit_link(link):
    """"
        Report that the given link has been visited. This visit will be linked in the database.
    """
    if find_link(link) is not None:
        num = int(link.split('-')[-1], base=16)
        run("UPDATE `links` SET visits = visits + 1 WHERE link=?", (num,))

def add_link(title, description=None, image=None):
    """
        Generate a new Rickroll link.
    """
    link = random.randint(0, 16**8 - 1)
    code = ('00000000' + hex(link)[2:])[-8:]
    while find_link(hex(link)[2:]) is not None:  
        print(f"{code} already exists.")  
        link = random.randint(0, 16**8 - 1)
        code = ('00000000' + hex(link)[2:])[-8:]

    run(
        "INSERT INTO `links` (`link`, `title`, `description`, `image`) VALUES (?, ?, ?, ?);", 
        (link, title, description, image)
    )
    return code


def find_link(link):
    """
        Looks for an entry in the database that matches the description.
        If it doesn't exist, it returns None.
    """
    try:
        key = link.split('-')[-1]
        num = int(key, base=16)
    except ValueError:
        return None

    for answer in run("SELECT * FROM `links` WHERE link=?", (int(key, base=16),))():
        return answer
    else:
        return None

def run(query, args=None):
    """
        Run a query on the database.
        Since threads do not pass on variables, a new SQLite connection is made.
    """
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    if args is None:
        c.execute(query)
    else:
        c.execute(query, args)
    
    conn.commit()

    # Return a generator that iterates over 
    def output():
        while True:
            q = c.fetchone()
            if q is None:
                break

            yield q
        conn.close()
    return output


def count_rickrolls() -> int:
    """
        Calculate how many times someone has been rickrolled by the website.
    """
    try:
        for answer in run("SELECT SUM(visits) FROM links;")():
            if answer[0] is None:
                raise ValueError(
                    "No rickrolls detected. Database is either new or corrupted."
                )
            return answer[0]
        else:
            return 0
    except sqlite3.OperationalError as e:
        print(e)
        return 0
    except Exception as e:
        print(e)
        return 0
