# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
#The script provides all NB API for CSSM Server necessary for Smart Licensing 
import requests
from argparse import ArgumentParser
import json

def getToken(client_id, client_secret):
    """ This proc will return username/password for Stage CSSM for APIs"""
    logm = ""
    
    # For Production CSSM
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    
    querystring = {"client_id":client_id,"client_secret":client_secret,"grant_type":"client_credentials"}
    headers = {'Cache-Control': "no-cache", 'Postman-Token': "7738e018-f7da-8777-3db5-821f52dd6352"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    try:
        token_type = response.json()['token_type']
        access_token = response.json()['access_token']
    except:
        logm = 'Unable to get the usr/pwd for Stage CSSM. Error:  %s' % response.text
        return logm

    usr_pwd = ' '.join((token_type, access_token))

    return str(usr_pwd)