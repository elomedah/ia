from rag.loaders import load_corpus, remove_repeated_lines


def test_corpus_loads_all_formats(corpus_dir):
    docs = load_corpus(corpus_dir)
    types = {d.metadata["type"] for d in docs}
    assert {"md", "txt", "pdf", "html"} <= types
    assert all(d.text.strip() for d in docs)


def test_pdf_header_footer_removed(corpus_dir):
    pdf_pages = [d for d in load_corpus(corpus_dir) if d.metadata["type"] == "pdf"]
    assert len(pdf_pages) == 2
    for page in pdf_pages:
        assert "Usage interne" not in page.text          # en-tête répété
        assert "à usage pédagogique (module FM02) - page" not in page.text  # pied de page
    assert "150" in pdf_pages[0].text                    # le contenu est conservé


def test_remove_repeated_lines_keeps_unique_content():
    pages = ["ENTETE\nA\nPied 1", "ENTETE\nB\nPied 2", "ENTETE\nC\nPied 3"]
    assert remove_repeated_lines(pages) == ["A", "B", "C"]


def test_html_cleaned(corpus_dir):
    html = [d for d in load_corpus(corpus_dir) if d.metadata["type"] == "html"][0]
    assert "Plan du site" not in html.text               # footer retiré
    assert "Annuaire" not in html.text                   # menu de navigation retiré
    assert "# Onboarding IT" in html.text                # titres convertis en Markdown
    assert "9 h 30" in html.text
