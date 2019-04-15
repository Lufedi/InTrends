import requests
import pickle
import logging

import linkedin_api.settings as settings

logger = logging.getLogger(__name__)


class ChallengeException(Exception):
    logger.info(Exception)


class UnauthorizedException(Exception):
    pass


class Client(object):
    """
    Class to act as a client for the Linkedin API.
    """

    # Settings for general Linkedin API calls
    API_BASE_URL = "https://www.linkedin.com/voyager/api"
    REQUEST_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/66.0.3359.181 Safari/537.36",
            ]
        ),
        # "accept": "application/vnd.linkedin.normalized+json+2.1",
        "accept-language": "en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-li-lang": "en_US",
        "x-restli-protocol-version": "2.0.0",
        # "x-li-track": '{"clientVersion":"1.2.6216","osName":"web","timezoneOffset":10,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
    }

    # Settings for authenticating with Linkedin
    AUTH_BASE_URL = "https://www.linkedin.com"
    AUTH_REQUEST_HEADERS = {
        "X-Li-User-Agent": "LIAuthLibrary:3.2.4 \
                            com.linkedin.LinkedIn:8.8.1 \
                            iPhone:8.3",
        "User-Agent": "LinkedIn/8.8.1 CFNetwork/711.3.18 Darwin/14.0.0",
        "X-User-Language": "en",
        "X-User-Locale": "en_US",
        "Accept-Language": "en-us",
        "cookie": f'bcookie="v=2&8979ec6e-77f0-459d-8725-06fa754a85e0"; bscookie="v=1&20181227192724e8ad6827-8e00-4caa-8816-44d38cc7ad86AQEhnOoJVDz2K9c7zMtB0aUte5bdmWzu"; _ga=GA1.2.1290526053.1546130182; _guid=1f130f8e-10b5-46eb-8608-910b66396824; li_oatml=AQHNFeKsf7WTwwAAAWoGHwa1qudf0BJ8MKOg6FvAUOA2m9Ev1j2DZIbhye_sFymOPhoBz5CcliF9pN7elVnFaU48K3m2gayg; aam_uuid=42108163156549490870948759212049868622; VID=V_2019_04_13_16_430454; visit=v=1&M; JSESSIONID="ajax:8585180457151008895"; sl=v=1&udiYU; liap=true; li_at=AQEDASuLyVsD7TpMAAABahqueXYAAAFqPrr9dk4Af__xD1YHj4Qi39IeWN3IFLTewvARcBsRTmEA2JjisIEGC0owvW4R9Aq-bTdTlMHZYNuSKZCUoujUwZU4vG-oUDnWCExgSeaaQ0AWg0Ebk0KprfGE; lang=v=2&lang=es-es; _lipt=CwEAAAFqH3p7POba_qe3xquhj0VpZodtr_obdaBjY8u9ZH7kG7ZldG7C0dX6JRhOq_WiSaWlhTtLfGU21K5NEv__3c1zpjxF5sGumOfZxSsdnDeuSezj450; SID=c36769ef-3693-44d6-87bf-98e36f45e6f0; _gat=1; UserMatchHistory=AQLPN2h3mEJ9DwAAAWofh7MB26H-U9-CC4FLWjdeM1YXRgtQHluU8F4HThzQea0_GMizLx_GQGPKgCz2MQOAjR-IO7HTPtxMAp-EkZc-gmzSg4GV-FOE4a5LXA603HpzU7kHe5hxDZzOXo-knUWyXfCT2Jtttjc7l66vRZCywCifn2vmWrOTRXYCPQOgv2JrjlgLB1aGkPV7xVDHVp0KiOETlJUAAwanAcst; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-1303530583%7CMCIDTS%7C18002%7CMCMID%7C42246536548095577801001351931554059397%7CMCAAMLH-1555911872%7C7%7CMCAAMB-1555911872%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1555314272s%7CNONE%7CMCCIDH%7C-1777838976%7CvVersion%7C3.3.0; lidc="b=TGST05:g=1342:u=1:i=1555307171:t=1555312024:s=AQH2VOQyy2KoeCaJH8a8mOZWWgl80OLi"'
    }

    def __init__(self, debug=False, refresh_cookies=False):
        self.session = requests.session()
        self.session.headers = Client.REQUEST_HEADERS

        self.logger = logger
        self._use_cookie_cache = not refresh_cookies
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def _request_session_cookies(self):
        """
        Return a new set of session cookies as given by Linkedin.
        """
        if self._use_cookie_cache:
            self.logger.debug("Attempting to use cached cookies")
            try:
                with open(settings.COOKIE_FILE_PATH, "rb") as f:
                    cookies = pickle.load(f)
                    if cookies:
                        return cookies
            except FileNotFoundError:
                self.logger.debug("Cookie file not found. Requesting new cookies.")

        res = requests.get(
            f"{Client.AUTH_BASE_URL}/uas/authenticate",
            headers=Client.AUTH_REQUEST_HEADERS,
        )

        return res.cookies

    def _set_session_cookies(self, cookiejar):
        """
        Set cookies of the current session and save them to a file.
        """
        self.session.cookies = cookiejar
        self.session.headers["csrf-token"] = self.session.cookies["JSESSIONID"].strip(
            '"'
        )
        with open(settings.COOKIE_FILE_PATH, "wb") as f:
            pickle.dump(cookiejar, f)

    def authenticate(self, username, password):
        """
        Authenticate with Linkedin.

        Return a session object that is authenticated.
        """
        self._set_session_cookies(self._request_session_cookies())

        payload = {
            "session_key": username,
            "session_password": password,
            "JSESSIONID": self.session.cookies["JSESSIONID"],
        }

        res = requests.post(
            f"{Client.AUTH_BASE_URL}/uas/authenticate",
            data=payload,
            cookies=self.session.cookies,
            headers=Client.AUTH_REQUEST_HEADERS,
        )

        data = res.json()
        logger.info(self.session.cookies)
        logger.info('data')
        logger.info(data)
        if data and data["login_result"] != "PASS":
            raise ChallengeException(data["login_result"])

        if res.status_code == 401:
            raise UnauthorizedException()

        if res.status_code != 200:
            raise Exception()
        self._set_session_cookies(res.cookies)
