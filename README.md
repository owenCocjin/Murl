# <u>Murl</u><br><sub>(mee-YUR-uhl)</sub>

> MITM attack that loads a requested page served by you. This means the user can use and request any site, but the page will be hosted on your hardware, allowing control over user's experience

---

## Instructions
- Run command in Murl directory: `sudo ./murl.py`. The script default runs on any interface, port 80
- The url should be in the format: `<local address>/?url=<full target url>.` A working example is, on the serving computer, go to a browser and enter the URL: `localhost/?url=https://youtube.com`

## Known Bugs
- Server crashes if request attempt without target URL
- (Apparently) Random missing icons
- Pages fail to load when requested relatively (`http://localhost/bad_page.js` vs `http://target_page.com/bad_page.js`)

## Dependencies
- [Sockets](https://docs.python.org/3/howto/sockets.html)
- [Requests](https://requests.readthedocs.io/en/master/)

## Future Implementations:
- Make Murl change the url to appear as if it was coming from the legitimate URL, snuffing suspicion
- Add persistent connections from client to Murl, and from Murl to target server
- Allow user to change links before page is served to target user

## Terminology
> Just some terms I'll use to make sure we're all on the same page!

- Murl: This script/the server this script creates
- User: The person running the Murl script
- Target URL: The URL the Murl will me impersonating
- Target User: The client that Murl will be serving
