class Booker(threading.Thread):
    def __init__(self, fname, lname, email, start, end, room, submit=False):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.start = start
        self.end = end
        self.room = room
        self.submit = submit
    def run(self):
        book(self.fname, self.lname, self.email, self.start, self.end,
             self.room, self.submit)

