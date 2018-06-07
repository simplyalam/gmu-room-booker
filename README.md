# GMU Study Room Booker

Automated booking for students at GMU. Books any study room located at https://library.gmu.edu/use/study-rooms. Each student is capped to 4 hour blocks by GMU. The booker is capable of simultaneously booking multiple blocks, if provided with multiple student credentials.

## Getting Started

1. Install Selenium
2. Edit main.py to include student(s) credentials.
3. Run main.py and the room will be booked 1 week ahead at 12pm.

### Prerequisites

Selenium
```
pip install selenium
```

### Running

A Booker is initialized with 5 fields. First name, last name, GMU email, start time, end time, and room number.
Start and end times must be provided in 24 hour format.
```
student1 = Booker('First', 'Last', 'flast@masonlive.gmu.edu', 11, 15, '4001')
```

## Built With
* [Python 3.6](https://www.python.org/downloads/)
* [Selenium](https://seleniumhq.github.io/selenium/docs/api/py/) - The web browser automation tool used

## Authors

* **Albert Lam** - *All the work* - [simplyalam](https://github.com/simplyalam)

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Selenium for building an amazing web automation tool
