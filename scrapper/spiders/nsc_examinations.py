import logging
import os
import uuid

import scrapy
from scrapy.http import TextResponse

logger = logging.getLogger(__name__)

output_dir = os.getenv("NSC_EXAMINATIONS_DIR", "nsc-examinations")
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


class NSCExaminationsSpider(scrapy.Spider):
    name = "nsc_examinations"
    start_urls = [
        "https://www.education.gov.za/Curriculum/NationalSeniorCertificate(NSC)Examinations.aspx"
    ]

    def parse(
        self: "NSCExaminationsSpider", response: TextResponse, **kwargs
    ) -> None:
        # Previous exam papers (Gr 10, 11 & 12)
        for exam_papers_link in response.css("div#dnn_ctr1741_ContentPane a"):
            yield response.follow(exam_papers_link, self.parse)

        for download_link in response.css("td.DownloadCell a"):
            yield response.follow(download_link, self.save_pdf)

    @staticmethod
    def save_pdf(response: TextResponse) -> None:
        with open(os.path.join(output_dir, "%s.%s" % (uuid.uuid4().hex, "pdf")), "wb") as pdf:
            pdf.write(response.body)
