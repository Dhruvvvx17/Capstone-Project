from libraries import *
from hdf_links import *


class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

   # Overrides from the library to keep headers when redirected to or from
   # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


def download_hdf(hdf_list):
    username = "devb"
    password = "Devearthdata@183"

    # Session variable using credentions with custom request class
    session = SessionWithHeaderRedirection(username, password)

    for url in urls:

        # extract the filename from the url to be used when saving the HDF file
        filename = url[url.rfind('/')+1:]
        image_date = '_'.join(url[url.rfind('/')-10:url.rfind('/')].split('.'))

        try:
            # submit the request using the session
            response = session.get(url, stream=True)
            print(f"{filename} status code: {response.status_code}")

            # raise an exception in case of http errors
            response.raise_for_status()

            # Download and save the HDF file
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)

                print(filename + " Download complete!")

            return filename

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print(filename + " Error Occured: ", e)

            exit()
