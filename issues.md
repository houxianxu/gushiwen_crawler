### Here is some implement details for this crawler

1. `LOG_LEVEL = 'INFO'` in `settings.py`, because I don't want to print item in terminal. The command `scrapy crawl myproject` it print all item and all degub log by default.

2. Set `response = response.replace(body=response.body.replace('<br>', '\n'))` before using response. Because the target HTML use `<br>` to separate different paragraphs. e.g.(bfanyi_1)

3. Get `div_text_list = response.xpath('//div[@class="shileft"]//div[@class="shangxicont"]/text()').extract()` before crawling `<p></p>`. This is because in some HTML documents, the **content** is located in `<div></div>` not `<p></p>` e.g.(bfanyi_764).

4. http://so.gushiwen.org/fanyi_694.aspx, example for Baidu Translation.

