from booker import Booker

book_threads = [
    Booker('First', 'Last', 'flast@masonlive.gmu.edu', 8, 12, '4001'),
    Booker('First2', 'Last2', 'flast2@masonlive.gmu.edu', 12, 15, '4001')
]

for b in book_threads:
    b.start()

for b in book_threads:
    b.join()

print('Exiting Booker')
