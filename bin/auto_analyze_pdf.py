import sys, os
sys.path.append(".")
from community.db import session_scope, ArxivModel
from community.analyzer import PDFAnalyzer
from community.settings import PDF_PATH
from sqlalchemy import desc
from argparse import ArgumentParser
import logging
import time
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--forever", action="store_true")
    args = ap.parse_args()
    analyzer = PDFAnalyzer()
    with session_scope() as session:
        run_flag = True
        while run_flag:
            papers = session.query(ArxivModel).filter(ArxivModel.analyzed.is_(False)).order_by(desc(ArxivModel.published_time)).limit(20).all()
            for paper in papers:
                pdf_url = paper.pdf_url + ".pdf"
                pdf_fn = os.path.basename(pdf_url)
                save_path = "{}/{}".format(PDF_PATH, pdf_fn)
                if not os.path.exists(save_path):
                    logging.info("download {}".format(pdf_fn))
                    os.system("wget -O {} --user-agent=Lynx {}".format(save_path, pdf_url))
                    time.sleep(1)
                result = analyzer.run(save_path)
                if not result:
                    raise SystemError
                if result["introduction"]:
                    paper.introduction = result["introduction"].replace("\0", "")
                if result["conclusion"]:
                    paper.conclusion = result["conclusion"].replace("\0", "")
                paper.analyzed = True
                logging.info("{} INTRO:{} CONCLUSION:{}".format(paper.pdf_url, "o" if result["introduction"] else "x", "o" if result["conclusion"] else "x"))
            session.commit()
            if not args.forever:
                # beak
                run_flag = False
