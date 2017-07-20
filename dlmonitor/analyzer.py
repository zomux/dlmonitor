import os, sys
import re

TMP_PATH = "/tmp/analyzed_pdf.txt"
OUTLINE_PATH = "/tmp/analyzed_pdf_outline.txt"

class PDFAnalyzer(object):
    """
    Analyze the content of PDF files.
    This class relies on PDFminer.
    """

    def run(self, path):
        """
        Extract introduction and conslusion text from PDF.
        """
        if not os.path.exists(path):
            return None
        os.system("pdf2txt.py {} > {}".format(path, TMP_PATH))
        os.system("dumppdf.py -T {} > {}".format(path, OUTLINE_PATH))
        if not os.path.exists(TMP_PATH) or not os.path.exists(OUTLINE_PATH):
            return None
        # Extract outlines
        outline_content = open(OUTLINE_PATH).read()
        titles = re.findall(r'title="([^"]+)"', outline_content)
        if titles:
            return self.extract_with_outline(titles)
        else:
            return self.extract_without_outline()

    def extract_with_outline(self, titles):
        """
        Actually, with an outline, any section can be extracted easily.
        """
        titles.append("References") # Manually add a section, in case missing refrence section
        intro_titles = filter(lambda t: "introduction" in t.lower(), titles)
        conclusion_titles = filter(lambda t: "conclusion" in t.lower(), titles)
        if intro_titles:
            intro_title = intro_titles[0]
            intro_words = intro_title.split()
            alter_intro_title = " ".join(intro_words[1:]) if len(intro_words) > 1 else intro_title
            intro_word_n = len(intro_title.split())
            for idx in range(titles.index(intro_title) + 1, len(titles)):
                intro_end_title = titles[idx]
                if intro_end_title.count(".") > intro_title.count("."):
                    continue
                words = intro_end_title.split()
                alter_intro_end_title = " ".join(words[1:]) if len(words) > 1 else intro_end_title
                intro_end_word_n = len(intro_end_title.split())
                break
        else:
            intro_title = None
            intro_word_n = 0
        if conclusion_titles:
            conclusion_title = conclusion_titles[-1]
            words = conclusion_title.split()
            alter_conclusion_title = " ".join(words[1:]) if len(words) > 1 else conclusion_title
            conclusion_word_n = len(conclusion_title.split())
            for idx in range(titles.index(conclusion_title) + 1, len(titles)):
                conclusion_end_title = titles[idx]
                if conclusion_end_title.count(".") > conclusion_end_title.count("."):
                    continue
                words = conclusion_end_title.split()
                alter_conclusion_end_title = " ".join(words[1:]) if len(words) > 1 else conclusion_end_title
                conclusion_end_word_n = len(conclusion_end_title.split())
                break
        else:
            conclusion_title = None
            conclusion_word_n = 0
        # Analyze lines, just in the same manner of the code without outlines
        # So, may be the two functions can be merged
        lines = open(TMP_PATH).readlines()
        intro_buf = ""
        conclusion_buf = ""
        intro_success = False
        conclusion_success = False
        mode = "none"
        skipping = False
        for line in lines:
            line = line.strip()
            words = line.split()
            if mode == "none" and intro_title and abs(len(words) - intro_word_n) <= 1 and (
                    intro_title in line or intro_title.upper() in line or
                    alter_intro_title in line or alter_intro_title.upper() in line
                ):
                mode = "introduction"
            elif (mode == "introduction" and abs(len(words) - intro_end_word_n) <= 1 and (
                    intro_end_title in line or intro_end_title.upper() in line or
                    alter_intro_end_title in line or alter_intro_end_title.upper() in line
                )):
                mode = "none"
                intro_success = True
            elif mode == "none" and conclusion_title and abs(len(words) - conclusion_word_n) <= 1 and (
                    conclusion_title in line or conclusion_title.upper() in line or
                    alter_conclusion_title in line or alter_conclusion_title.upper() in line
                ):
                mode = "conclusion"
            elif (mode == "conclusion" and abs(len(words) - conclusion_end_word_n) <= 1 and (
                    conclusion_end_title in line or conclusion_end_title.upper() in line or
                    alter_conclusion_end_title in line or alter_conclusion_end_title.upper() in line
                )):
                mode = "none"
                conclusion_success = True
            elif mode != "none":
                # Recording mode
                if skipping and len(words) > 1 and line[-1] != ".":
                    continue
                else:
                    skipping = False
                # Skip one-word lines
                if len(words) <= 1: continue
                # Skip Table, Figure
                if line.startswith("Figure ") or line.startswith("Table "):
                    if line[-1] != ".":
                        skipping = True
                    continue
                if mode == "introduction":
                    intro_buf += line + " "
                elif mode == "conclusion":
                    conclusion_buf += line + " "
        ret = {
            "introduction": intro_buf if intro_success else None,
            "conclusion": conclusion_buf if conclusion_success else None
        }
        return ret

    def extract_without_outline(self):
        """
        No outline, just extract with hand-craft rules written by Raphael Shu.
        Success rate: 15%.
        """
        lines = open(TMP_PATH).readlines()
        intro_buf = ""
        conclusion_buf = ""
        intro_success = False
        conclusion_success = False
        mode = "none"
        skipping = False
        for line in lines:
            line = line.strip()
            words = line.split()
            if mode == "none" and line == "Introduction" or len(words) <= 3 and (
                line == "1 Introduction" or line == "1. Introduction" or line == "I. Introduction"
            ):
                mode = "introduction"
            elif (mode == "introduction" and (
                    (len(words) == 6 and (words[0] == "2" or words[0] == "2." or words[0] == "II.") and words[1][0] == words[1][0].upper())
                    or
                    (line == "Related Work")
                )):
                mode = "none"
                intro_success = True
            elif mode == "none" and len(words) <= 4 and len(words) >= 1 and (
                    words[0].startswith("Conclusion")
                    or
                    (len(words) > 1 and words[1].startswith("Conclusion"))
                ):
                mode = "conclusion"
            elif mode == "conclusion" and line == "References":
                mode = "none"
                conclusion_success = True
            elif mode != "none":
                # Recording mode
                if skipping and len(words) > 1 and line[-1] != ".":
                    continue
                else:
                    skipping = False
                # Skip one-word lines
                if len(words) <= 1: continue
                # Skip Table, Figure
                if line.startswith("Figure ") or line.startswith("Table "):
                    if line[-1] != ".":
                        skipping = True
                    continue
                if mode == "introduction":
                    intro_buf += line + " "
                elif mode == "conclusion":
                    conclusion_buf += line + " "
        ret = {
            "introduction": intro_buf if intro_success else None,
            "conclusion": conclusion_buf if conclusion_success else None
        }
        return ret
