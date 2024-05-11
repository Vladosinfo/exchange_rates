import platform
import sys
# import aiohttp
import asyncio
# from classes.Request_rates import Request_rates as request
from classes.Request_rates import Request_rates
from classes.Json_format import Json_format
from classes.Client import Client
from abstract_classes.request_data import Request_data
from datetime import datetime, timedelta

url_template = 'https://api.privatbank.ua/p24api/exchange_rates?date='


async def get_rate(url):
    client = Client(Request_rates, url)
    data = await client.get_data()

    json_format = Json_format(data)
    course = await json_format.generate()

    return course


async def main(count = None): 
    cources = []
    current_datetime = datetime.now().strftime("%d.%m.%Y")
    url = url_template + current_datetime
      
    print(f"reading rages for date: {current_datetime}")
    course = await get_rate(url)
    cources.append(course)

    count = int(count)
    cur_date = datetime.now()
    if count > 1:
        for i in range(1, count):
            for_days_interval = timedelta(days=i)
            date_before_for_days_ = (cur_date - for_days_interval).strftime("%d.%m.%Y")
            print(f"reading rages for date: {date_before_for_days_}")
            url = url_template + date_before_for_days_
            course = await get_rate(url)
            cources.append(course)

    return cources


if __name__ == "__main__":
    main_arg = 0
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric() and int(sys.argv[1]) < 11 and int(sys.argv[1]) > 1:
            main_arg = sys.argv[1]
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(main_arg))
    print(r)