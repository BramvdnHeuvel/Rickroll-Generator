# Rickroll Generator

This is the [Rickroll Generator](https://rr.noordstar.me/), a website that allows people to creat new Rickroll links for people to fall for! The link includes a rich preview to deceive your victims even more!

[What is a rickroll?](https://en.wikipedia.org/wiki/Rickrolling)


## Setup

To set the program up, run
```
    pip install -r requirements.txt
    python setup.py
```

To run the website, run
```
    python main.py 127.0.0.1 5000
```
where `127.0.0.1` and `5000` are the wished ip-address and port, respectively.

If you want to use your own domain name (and not ours), then change line 7 in the file `main.py` to your own domain name. **Make sure you do not add a / at the end of the domain.**
