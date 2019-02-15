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

def checkLicenseAvailability(auth_code, sa_domain, vAccount, licenseName="C9300 Network Advantage", licenseCount=1):
    """This proc check if <licenseCounbt> are available under a given <VA> """
    url = "https://apx.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{smartAccountDomain}/licenses"
    payload = "{\"virtualAccounts\": [\"%s\"],\"limit\": 50,\"offset\": 0}" %(vAccount)
    #payload = payload.format(domain=sa_domain)
    logm = ""
    headers = {
    'content-type': "application/json",
    'Authorization': "",
    'cache-control': "no-cache",
    }
    headers['Authorization'] = auth_code
    response = requests.request("POST", url.format(smartAccountDomain=sa_domain), headers=headers, data=payload)

    try:
        out = json.loads(response.text)
    except:
        logm = 'Unable to get the response from CSSM. Error:  %s' % response.text
        return(logm)

    licenseTypeExists = False
    licenseList = []
    for license in out["licenses"]:
        licenseList.append(license['license'])
        if license['license'].upper() ==  licenseName.upper():
            licenseTypeExists = True
            licenseAvailable = license['available']
            break 

    if not licenseTypeExists:
        print("license %s does not exist! available licenseTypes is %s" %(licenseName, licenseList))
        returnvar = False

    elif licenseAvailable >= licenseCount:
        returnvar = True

    else:
        print("Looking for %s licenses and only %s available" %(licenseCount, licenseAvailable))
        returnvar = False

    return returnvar

def generateToken(auth_code, sa_domain, virtualAccount):

    url = "https://apx.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{account_domain}/virtual-accounts/{virtual_account}/tokens"
    logm = ""
    payload = "{ \"description\":\"this is an auto generated token via script\", \"expiresAfterDays\":30,\"exportControlled\":\"Not Allowed\", \"limit\": 50,\"offset\": 0}"

    headers = {
    'content-type': "application/json",
    'Authorization': "",
    'cache-control': "no-cache",
    }
    headers['Authorization'] = auth_code
    response = requests.request("POST", url.format(account_domain=sa_domain, virtual_account=virtualAccount), headers=headers, data=payload)
    try:
        out = json.loads(response.text)
    except:
        logm = 'Unable to get the response from CSSM. Error:  %s' % response.text
        return(logm)

    if out['status'] == 'SUCCESS':
        token = out['tokenInfo']['token']

    else:
        token = False

    return token