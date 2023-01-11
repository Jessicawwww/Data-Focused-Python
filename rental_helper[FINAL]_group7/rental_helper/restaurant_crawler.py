import pandas as pd
import requests
from bs4 import BeautifulSoup


def create_restaurant_csv():
    #downloaded urls (cannot scrape from the website for changing labels)
    urls=['https://www.zomato.com/adelaide/parwana-afghan-restaurant-torrensville/info','https://www.zomato.com/adelaide/ruby-red-flamingo-north-adelaide/info','https://www.zomato.com/adelaide/eggless-goodwood/info','https://www.zomato.com/adelaide/ur-caffe-north-adelaide/info','https://www.zomato.com/adelaide/a-hereford-beefstouw-city-centre/info','https://www.zomato.com/adelaide/yakitori-takumi-north-adelaide/info','https://www.zomato.com/adelaide/georges-on-waymouth-city-centre/info','https://www.zomato.com/adelaide/a-mothers-milk-parkside/info','https://www.zomato.com/adelaide/delicatessen-kitchen-and-bar-city-centre/info','https://www.zomato.com/adelaide/devour-cafe-patisserie-hilton/info','https://www.zomato.com/adelaide/the-greek-on-halifax-city-centre/info','https://www.zomato.com/adelaide/gauchos-city-centre/info','https://www.zomato.com/adelaide/ding-hao-restaurant-city-centre/info','https://www.zomato.com/adelaide/zest-cafe-gallery-glenelg/info','https://www.zomato.com/adelaide/froth-fodder-kurralta-park/info','https://www.zomato.com/adelaide/jasmin-indian-city-centre/info','https://www.zomato.com/adelaide/kaffana-city-centre/info','https://www.zomato.com/adelaide/little-nnq-city-centre/info','https://www.zomato.com/adelaide/roseys-unley/info','https://www.zomato.com/adelaide/kefi-greek-cuisine-glenelg-north/info','https://www.zomato.com/adelaide/est-pizzeria-city-centre/info','https://www.zomato.com/adelaide/red-ochre-north-adelaide/info','https://www.zomato.com/adelaide/dumpling-king-city-centre/info','https://www.zomato.com/adelaide/local-crowd-colonel-light-gardens/info','https://www.zomato.com/adelaide/pizza-e-mozzarella-bar-city-centre/info','https://www.zomato.com/adelaide/sosta-argentinian-kitchen-city-centre/info','https://www.zomato.com/adelaide/50sixone-hyde-park/info','https://www.zomato.com/adelaide/two-bit-villains-city-centre/info','https://www.zomato.com/adelaide/ajisen-ramen-1-city-centre/info','https://www.zomato.com/adelaide/pickle-in-the-middle-unley/info','https://www.zomato.com/adelaide/mamak-corner-city-centre/info','https://www.zomato.com/adelaide/public-city-centre/info','https://www.zomato.com/adelaide/the-topiary-cafe-tea-tree-gully/info','https://www.zomato.com/adelaide/nutrition-republic-hyde-park/info','https://www.zomato.com/adelaide/argo-on-the-square-city-centre/info','https://www.zomato.com/adelaide/abbots-and-kinney-city-centre/info','https://www.zomato.com/adelaide/mexican-society-city-centre/info','https://www.zomato.com/adelaide/whistle-flute-unley/info','https://www.zomato.com/adelaide/borsa-pasta-cucina-city-centre/info','https://www.zomato.com/adelaide/whipped-bake-bar-cafe-semaphore/info','https://www.zomato.com/adelaide/the-lion-hotel-north-adelaide/info','https://www.zomato.com/adelaide/the-ghan-kebab-house-blair-athol/info','https://www.zomato.com/adelaide/cafe-komodo-prospect/info','https://www.zomato.com/adelaide/low-slow-american-bbq-port-adelaide/info','https://www.zomato.com/adelaide/c-r-e-a-m-brighton/info','https://www.zomato.com/adelaide/zapatas-mexican-restaurant-north-adelaide/info','https://www.zomato.com/adelaide/il-toro-greenacres/info','https://www.zomato.com/adelaide/e-for-ethel-north-adelaide/info','https://www.zomato.com/adelaide/paddys-lantern-city-centre/info','https://www.zomato.com/adelaide/good-life-modern-organic-pizza-city-centre/info','https://www.zomato.com/adelaide/hawker-street-cafe-bowden/info','https://www.zomato.com/adelaide/parisis-restaurant-hyde-park-unley/info','https://www.zomato.com/adelaide/mr-bulgogi-mawson-lakes/info','https://www.zomato.com/adelaide/antica-pizzeria-e-cucina-unley/info','https://www.zomato.com/adelaide/the-market-shed-on-holland-city-centre/info','https://www.zomato.com/adelaide/beyond-india-north-adelaide/info','https://www.zomato.com/adelaide/coffee-institute-walkerville/info','https://www.zomato.com/adelaide/jerusalem-sheshkebab-house-city-centre/info','https://www.zomato.com/adelaide/papparich-city-centre/info','https://www.zomato.com/adelaide/the-annex-cafe-glenelg/info','https://www.zomato.com/adelaide/please-say-please-city-centre/info','https://www.zomato.com/adelaide/red-cacao-chocolatier-stirling/info','https://www.zomato.com/adelaide/the-playford-restaurant-city-centre/info','https://www.zomato.com/adelaide/regent-thai-north-adelaide/info','https://www.zomato.com/adelaide/kutchi-deli-parwana-city-centre/info','https://www.zomato.com/adelaide/union-hotel-city-centre/info','https://www.zomato.com/adelaide/chocolate-no-5-hahndorf/info','https://www.zomato.com/adelaide/303-by-the-sea-henley-beach/info','https://www.zomato.com/adelaide/candela-latin-american-food-goodwood/info','https://www.zomato.com/adelaide/bracegirdles-glenelg/info','https://www.zomato.com/adelaide/godi-la-vita-hyde-park/info','https://www.zomato.com/adelaide/jennys-gourmet-bakery-eastwood/info','https://www.zomato.com/adelaide/trouble-and-strife-goodwood/info','https://www.zomato.com/adelaide/the-little-eastern-saint-morris/info','https://www.zomato.com/adelaide/the-strand-cafe-restaurant-1-glenelg/info','https://www.zomato.com/adelaide/boatshed-cafe-hallett-cove/info','https://www.zomato.com/adelaide/pho-linh-salisbury-north/info','https://www.zomato.com/adelaide/la-madeleine-norwood/info','https://www.zomato.com/adelaide/clever-little-tailor-city-centre/info','https://www.zomato.com/adelaide/five-little-figs-payneham-south/info','https://www.zomato.com/adelaide/saigon-gate-kilburn/info','https://www.zomato.com/adelaide/t-chow-city-centre/info','https://www.zomato.com/adelaide/jimmies-restaurant-crafers/info','https://www.zomato.com/adelaide/loucas-seafood-grill-city-centre/info','https://www.zomato.com/adelaide/cafe-brunelli-city-centre/info','https://www.zomato.com/adelaide/coffylosophy-city-centre/info','https://www.zomato.com/adelaide/botanic-gardens-restaurant-city-centre/info','https://www.zomato.com/adelaide/gusto-ristorante-norwood/info','https://www.zomato.com/adelaide/sir-cafe-1-city-centre/info','https://www.zomato.com/adelaide/long-lost-friend-kensington-gardens/info','https://www.zomato.com/adelaide/queens-head-hotel-north-adelaide/info','https://www.zomato.com/adelaide/tongue-thaid-mile-end/info','https://www.zomato.com/adelaide/stamps-mitcham/info','https://www.zomato.com/adelaide/the-pickled-duck-modbury/info','https://www.zomato.com/adelaide/gilbert-street-hotel-city-centre/info','https://www.zomato.com/adelaide/thai-rosewater/info','https://www.zomato.com/adelaide/delhi-spice-marion/info','https://www.zomato.com/adelaide/the-boatdeck-cafe-pizzeria-mawson-lakes/info','https://www.zomato.com/adelaide/base-bar-norwood/info','https://www.zomato.com/adelaide/bricks-and-stones-adelaide/info','https://www.zomato.com/adelaide/mr-viet-city-centre/info','https://www.zomato.com/adelaide/48-flavours-city-centre/info','https://www.zomato.com/adelaide/zambrero-rundle-street-city-centre/info','https://www.zomato.com/adelaide/taste-of-nepal-beulah-park/info','https://www.zomato.com/adelaide/european-cafe-norwood/info','https://www.zomato.com/adelaide/goodies-grains-kitchen-1-city-centre/info','https://www.zomato.com/adelaide/samui-thai-hazelwood-park/info','https://www.zomato.com/adelaide/zaks-greek-restaurant-west-lakes/info','https://www.zomato.com/adelaide/beach-burrito-company-glenelg/info','https://www.zomato.com/adelaide/social-street-s-city-centre/info','https://www.zomato.com/adelaide/the-moseley-glenelg/info','https://www.zomato.com/adelaide/mayflower-restaurant-and-bar-city-centre/info','https://www.zomato.com/adelaide/villa-77-unley/info','https://www.zomato.com/adelaide/bar-9-central-city-centre/info','https://www.zomato.com/adelaide/caf%C3%A9-chennai-prospect/info','https://www.zomato.com/adelaide/bai-long-store-3-city-centre/info','https://www.zomato.com/adelaide/fellini-cafe-north-adelaide/info','https://www.zomato.com/adelaide/white-house-fortified-food-wine-hahndorf/info','https://www.zomato.com/adelaide/cafe-saba-norwood/info','https://www.zomato.com/adelaide/locavore-wine-bar-stirling/info','https://www.zomato.com/adelaide/taj-tandoor-city-centre/info','https://www.zomato.com/adelaide/aux-fines-bouches-brighton/info','https://www.zomato.com/adelaide/don-don-korean-bbq-buffet-city-centre/info','https://www.zomato.com/adelaide/hans-sushi-klemzig/info','https://www.zomato.com/adelaide/kent-town-hotel-the-jungle-restaurant-kent-town/info','https://www.zomato.com/adelaide/schnithouse-city-centre/info','https://www.zomato.com/adelaide/natures-providore-malvern/info','https://www.zomato.com/adelaide/feed-jetty-road-glenelg/info','https://www.zomato.com/adelaide/gringos-mexican-cantina-glenelg/info','https://www.zomato.com/adelaide/i-am-thai-marleston/info','https://www.zomato.com/adelaide/cafe-pellegrini-north-adelaide/info','https://www.zomato.com/adelaide/the-rolling-pin-bakery-patisserie-magill/info','https://www.zomato.com/adelaide/pasta-deli-glynde/info','https://www.zomato.com/adelaide/betel-leaf-cafe-seaton/info','https://www.zomato.com/adelaide/grotto-pizza-teca-norwood/info','https://www.zomato.com/adelaide/fair-espresso-city-centre/info','https://www.zomato.com/adelaide/yen-linh-croydon-park/info','https://www.zomato.com/adelaide/the-brompton-brompton/info','https://www.zomato.com/adelaide/warradale-hotel-warradale/info','https://www.zomato.com/adelaide/farina-00-pasta-wine-unley/info','https://www.zomato.com/adelaide/electra-house-hotel-city-centre/info','https://www.zomato.com/adelaide/cha-chis-mexican-cantina-glenunga/info','https://www.zomato.com/adelaide/abyssinian-restaurant-torrensville/info','https://www.zomato.com/adelaide/le-souk-city-centre/info','https://www.zomato.com/adelaide/montezumas-north-adelaide/info','https://www.zomato.com/adelaide/lezizz-eastwood/info','https://www.zomato.com/adelaide/burganomix-glenelg/info','https://www.zomato.com/adelaide/regattas-bistro-bar-city-centre/info','https://www.zomato.com/adelaide/petalumas-bridgewater-mill-bridgewater/info','https://www.zomato.com/adelaide/crema-on-jetty-glenelg/info','https://www.zomato.com/adelaide/kings-head-hotel-city-centre/info','https://www.zomato.com/adelaide/cafe-va-bene-campbelltown/info','https://www.zomato.com/adelaide/paesano-north-adelaide/info','https://www.zomato.com/adelaide/duthy-street-deli-unley/info','https://www.zomato.com/adelaide/korea-jung-city-centre/info','https://www.zomato.com/adelaide/the-lab-payneham/info','https://www.zomato.com/adelaide/simply-sushi-glenelg/info','https://www.zomato.com/adelaide/casuarina-malaysian-bistro-oaklands-park/info','https://www.zomato.com/adelaide/pancakes-at-the-port-port-adelaide/info','https://www.zomato.com/adelaide/hotaru-japanese-restaurant-city-centre/info','https://www.zomato.com/adelaide/mother-vine-wine-bar-city-centre/info','https://www.zomato.com/adelaide/the-watershed-mawson-lakes/info','https://www.zomato.com/adelaide/cinnamon-club-norwood/info','https://www.zomato.com/adelaide/inglewood-inn-houghton/info']

    datalist = []
    #get details from each html using bs4
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        data = []

        #get restaurant names
        names = soup.title.string
        namelist = names.split(',')
        name=namelist[0]

        #get cuisines
        cui = soup.find(attrs={'class': 'sc-rBLzX euEDKp'})
        cuisines = ''
        for child in cui:
            cuisines += child.a.string + ','
        cuisines = cuisines[:-1]

        #get opening time
        opening_time = soup.find(attrs={'class': 'sc-ebFjAB gFTiSD'})
        if opening_time is None:
            ot=''
        else:
            ot=opening_time.string

        #get contact details, marks and review number
        call = soup.find(attrs={'class': 'sc-1hez2tp-0 fanwIZ'}).string
        mark = soup.find(attrs={'class': 'sc-1q7bklc-1 cILgox'}).string
        review_number = soup.find(attrs={'class': 'sc-1q7bklc-8 kEgyiI'}).string

        #get restaurant location
        location_txt = soup.find(attrs={'class': 'sc-1hez2tp-0 clKRrC'}).string
        location_url = soup.find(attrs={'target': '_blank', 'rel': 'noopener noreferrer'}).attrs['href']
        location_latitude = location_url[51:65]
        location_longitude = location_url[66:80]

        #add information into record
        data.append(name)
        data.append(cuisines)
        data.append(ot)
        data.append(call)
        data.append(mark)
        data.append(review_number)
        data.append(location_txt)
        data.append(location_url)
        data.append(location_latitude)
        data.append(location_longitude)

        #add record into records list
        datalist.append(data)

    #save data
    df = pd.DataFrame(datalist)
    df.to_csv(r'backupcsv\restaurant1.csv', encoding="utf_8")

