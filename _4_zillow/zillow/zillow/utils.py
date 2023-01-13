from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode
import json


URL = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A25.855773%2C%22south%22%3A25.550068%2C%22east%22%3A-80.139157%2C%22west%22%3A-80.548696%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}&requestId=3'
COOKIE = 'x-amz-continuous-deployment-state=AYABeOcWMSQ39+G37TO09OkhJvAAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3NjA0OTUxU1JKRU1BTUNBQVQzAAEAAkNEABpDb29raWUAAACAAAAADHzBXkTisyfAwBSoBgAwfQAdzo8b0xU1L6eqjsrauZLw+ByC4o9KPPTiNdLECLOgQrualEVn6UHtmqV2M8KmAgAAAAAMAAQAAAAAAAAAAAAAAAAAACHGNm79veKys8skwC1Vk4b/////AAAAAQAAAAAAAAAAAAAAAQAAAAw8pXYot+A2GTEVRvkAtvwfXSkCuOkDsY5m26SP; optimizelyEndUserId=oeu1673010071885r0.4585676287725293; zgcus_aeut=AEUUT_31ea64a7-8dc2-11ed-943e-eea9eb4bbf31; zgcus_aeuut=AEUUT_31ea64a7-8dc2-11ed-943e-eea9eb4bbf31; zguid=24|$5986dd5f-32dc-4882-8a1d-37ac43efbb91; _ga=GA1.2.789748909.1673010074; _pxvid=32add791-8dc2-11ed-9060-436c4c747a44; zjs_user_id=null; zg_anonymous_id="acd51f34-1c67-4d50-9c14-84138486c00c"; _gcl_au=1.1.1403265666.1673010075; __pdst=89c2811cefb94a0982c287af4144dd36; _cs_c=0; _gid=GA1.2.1694093324.1673493884; zjs_anonymous_id="5986dd5f-32dc-4882-8a1d-37ac43efbb91"; _fbp=fb.1.1673493887056.146758386; _pin_unauth=dWlkPVpqWTNPVGhpTnpZdFpESTNNQzAwTUdRMUxUazFPVGt0TldKalpXTm1PREkzTnprNA; zgsession=1|02d9f5ab-d555-4ab6-a6ca-9f2cd0ffef3c; DoubleClickSession=true; pxcts=c7895d82-92fe-11ed-b01a-4c4d45477070; _hp2_ses_props.1215457233={"ts":1673585848447,"d":"www.zillow.com","h":"/"}; _clck=10lni07|1|f88|0; JSESSIONID=95DE73FE9CE8B1BCAF14039D3B48C110; g_state={"i_p":1673672263308,"i_l":2}; __gads=ID=122ef9bacec4683a:T=1673585929:S=ALNI_MYORjgY6u2OTjI4BIdYJFKIED7MSQ; __gpi=UID=00000ba32fd53381:T=1673585929:RT=1673585929:S=ALNI_MYfR-j0r_L-hJpf_iqhosp6zxwg1Q; _hp2_id.1215457233={"userId":"4002457752356240","pageviewId":"7618014998071663","sessionId":"2699938976192830","identity":null,"trackerVersion":"4.0"}; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_bsco=1; _px3=968071d81f2f5c32626a66aa193977c306f01725903865b4674df7d07d796928:yDO85c3GhoO8kDdO11JbLA3ubB3v2ZOiRH4ChbGMFXv2CKyxwWE0ia1JOV4fUxCpAVPcIEHvouKhr6uJXA+n4Q==:1000:GYzH6c9mMt4G+rlt2x/HfrW7ATCzUe8H4gf6MZtJkQimVyfpb4V5Flv2aRdG31U5rZEUSu0D2w3UcCYh2WNBJAC+/3q068pNfj8SydiL8GRcUTM6tQo2N7f94x4xSZ0fLKqMvyFFJ9WsXXAnCxXUFjOMLIxas4ajUffn2eIbB8yOCUoR85gXwrkDWayEh7yLhVahIoWC6jQyeOw6exw0Lg==; _uetsid=aa2e1e00922811ed97e487198af204d9; _uetvid=34a0daa08dc211ed82db7707055ea0fc; _gat=1; AWSALB=MILybLvP623B8cxqQmZ/V04mMRstd9fVk6qay34C8Xkadzp5gchsE6ca+Hsh2ij5gsMvkeTQMPEx/4k61ipJkmDiUTp3b2VI7cs5rNqmzst3H96kZhEPvMF1/eDZ; AWSALBCORS=MILybLvP623B8cxqQmZ/V04mMRstd9fVk6qay34C8Xkadzp5gchsE6ca+Hsh2ij5gsMvkeTQMPEx/4k61ipJkmDiUTp3b2VI7cs5rNqmzst3H96kZhEPvMF1/eDZ; search=6|1676179148326|rect=25.855773%2C-80.139157%2C25.550068%2C-80.548696&rid=12700&disp=map&mdm=auto&p=2&z=1&fs=1&fr=0&mmm=0&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0&featuredMultiFamilyBuilding=0&commuteMode=driving&commuteTimeOfDay=now		12700						; _clsk=4k9m0n|1673587148311|37|0|a.clarity.ms/collect'

def cookie_parser():
    cookie_string = COOKIE
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    
    return cookies

def parse_new_url(url,page_number):
    url_parsed = urlparse(url)
    query_string = parse_qs(url_parsed.query)
    search_query_state = json.loads(query_string.get('searchQueryState')[0])
    search_query_state['pagination'] = {"currentPage":page_number}

    query_string.get('searchQueryState')[0] = search_query_state
    encoded_qs = urlencode(query_string,doseq=1)
    new_url = f'https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}'

    return new_url 

