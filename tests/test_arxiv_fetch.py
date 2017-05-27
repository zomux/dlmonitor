import arxiv

print arxiv.query("cs.CL", prune=True, start=0, max_results=10)
