from flask import Flask, render_template
import requests

app = Flask(__name__)

symbols = [
    {"name": "عیار", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=34144395039913458&c=68%20&e=1"},
    {"name": "زر", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=33254899395816171&c=68%20&e=1"},
    {"name": "مثقال", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=32469128621155736&c=68%20&e=1"},
    {"name": "ناب", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=32469128621155736&c=68%20&e=1"},
    {"name": "زرفام", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=33144542989832366&c=68%20&e=1"},
    {"name": "طلا", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=46700660505281786&c=68%20&e=1"},
    {"name": "جواهر", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=38544104313215500&c=68%20&e=1"},
    {"name": "کهربا", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=25559236668122210&c=68%20&e=1"},
    {"name": "نفیس", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=4626686276232042&c=68%20&e=1"},
    {"name": "گوهر", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=12390706505809150&c=68%20&e=1"},
    {"name": "گنج", "url": "https://old.tsetmc.com/tsev2/data/instinfodata.aspx?i=58514988269776425&c=68%20&e=1"},
]


def fetch_data_and_extract_numbers():
    result_list = []

    for symbol in symbols:
        try:
            response = requests.get(symbol["url"])
            response.raise_for_status()

            data_array = response.text.split(',')
            payani = data_array[3]
            nav_ebtal = data_array[15]
            nav_ebtal = nav_ebtal.split(';')[0]

            result_list.append({
                "name": symbol["name"],
                "payani": payani,
                "nav_ebtal": nav_ebtal,
                "hobab_esmi": round(((int(payani) - int(nav_ebtal)) / int(nav_ebtal)) * 100, 2)
            })
        except requests.exceptions.RequestException as e:
            print(f"خطا در دریافت داده‌ها برای {symbol['name']}: {e}")

    sorted_results = sorted(result_list, key=lambda x: x["hobab_esmi"])
    return sorted_results


@app.route('/')
def index():
    results = fetch_data_and_extract_numbers()
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
