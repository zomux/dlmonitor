import sys, os
sys.path.append(".")
from dlmonitor.db import session_scope
from dlmonitor.db_models import WorkingQueueModel
from dlmonitor.latex import build_paper_html, retrieve_paper_html
from dlmonitor.settings import SOURCE_PATH
from sqlalchemy import desc
from argparse import ArgumentParser
from  sqlalchemy.sql.expression import func
import logging
import time
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--forever", action="store_true")
    args = ap.parse_args()
    with session_scope() as session:
        run_flag = True
        while run_flag:
            jobs = session.query(WorkingQueueModel).filter(WorkingQueueModel.type == "load_arxiv").order_by(func.random()).limit(5).all()
            logging.info("get {} jobs".format(len(jobs)))
            for job in jobs:
                arxiv_token = job.param
                if os.path.exists("{}/{}".format(SOURCE_PATH, arxiv_token)):
                    session.delete(job)
                    continue
                if not arxiv_token.startswith("19") and not arxiv_token.startswith("18"):
                    session.delete(job)
                    continue
                try:
                    build_paper_html(arxiv_token)
                except:
                    continue
                logging.info("built {}".format(arxiv_token))
                session.delete(job)
            session.commit()
            if not jobs:
                time.sleep(3)
            if not args.forever:
                # beak
                run_flag = False
