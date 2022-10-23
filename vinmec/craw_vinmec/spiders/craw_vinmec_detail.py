import scrapy

class Ds_Benh_Spider(scrapy.Spider):
    name = "ds_benh"  # tên của spider
    allowed_domains = ["vinmec.com"]  # dont't config https://www...
    # Homepage chứa đường dẫn tời các bệnh
    start_urls = [
        'https://vinmec.com/vi/benh/',
    ]
    keyword_list = ["tiêu hoá",
                    "hệ tiêu hoá",
                    "đường ruột",
                    "tiêu chảy",
                    "đau dạ dày",
                    "đại tràng",
                    "hoành tá tràng",
                    "ruột non",
                    "ruột thừa",
                    "viêm ruột",
                    "hệ vi sinh cân bằng",
                    "khó tiêu",
                    "táo bón",
                    "thực quản",
                    "ruột kích thích",
                    "men vi sinh",
                    "cân bằng hệ vi sinh",
                    "hệ vi sinh đường ruột",
                    "hệ vi sinh",
                    "sử dụng men vi sinh",
                    "men vi sinh dạng ống",
                    "chủng men vi sinh",
                    "men vi sinh đa chủng",
                    "tiêu hóa khỏe",
                    "men vi sinh 10 chủng",
                    "men vi sinh BioGaia ",
                    "chảy máu tiêu hóa",
                    "rối loạn tiêu hóa",
                    "đường tiêu hóa",
                    "bệnh đường tiêu hóa",
                    "dạ dày"]
    # for từng bệnh
    # def parse(self, response):

    #     # lay ra cac element co chua link toi benh
    #     # list_benh = response.css(".collapsible-target > li ")
    #     for list_benh in response.css(".collapsible-target > li "):
    #         yield {
    #             'ten_benh': list_benh.css('a::text').get(),
    #             'url': list_benh.css('a').attrib['href'],
    #         }

    def parse(self, response):

        # lay ra cac element co chua link toi benh
        # list_benh = response.css(".collapsible-target > li ")
        for list_benh in response.css(".collapsible-target > li "):
            url = list_benh.css('a').attrib['href']
            yield scrapy.Request(response.urljoin(url), callback=self.get_detail)

    def get_detail(self, response):
        item = []
        is_benh_tieu_hoa = False
        for paragraph in response.css(".collapsible-container"):
            dct = {}
            dct["van_de"] = paragraph.css('h2>span::text').get()
            dct["tra_loi"] = paragraph.css("ul>li ::text, p ::text").getall()
            if any(substring in dct["van_de"] for substring in self.keyword_list) \
                or any(substring in dct["tra_loi"] for substring in self.keyword_list):
                    is_benh_tieu_hoa = True
            item.append(dct)
        if is_benh_tieu_hoa is True:
            output = {}
            output["id-benh"] = str(response.request.url).split("/")[-2]
            output["cac-van-de-lien-quan"] = item
            yield output
            
    