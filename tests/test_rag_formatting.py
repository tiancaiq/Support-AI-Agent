import unittest

from langchain_core.documents import Document

from rag.formatting import append_sources, build_context, format_sources


class RagFormattingTest(unittest.TestCase):
    def test_build_context_numbers_each_document(self):
        docs = [
            Document(page_content="Clean the charging contacts.", metadata={"source": "data/maintenance_guide.txt"}),
            Document(page_content="Clear obstacles near the dock.", metadata={"source": "data/robot_vacuum_faq.txt"}),
        ]

        context = build_context(docs)

        self.assertIn("[data 1]", context)
        self.assertIn("Clean the charging contacts.", context)
        self.assertIn("[data 2]", context)
        self.assertIn("data/robot_vacuum_faq.txt", context)

    def test_format_sources_deduplicates_document_names(self):
        docs = [
            Document(page_content="A", metadata={"source": "/tmp/data/maintenance_guide.txt"}),
            Document(page_content="B", metadata={"source": "/tmp/data/maintenance_guide.txt"}),
            Document(page_content="C", metadata={"source": "/tmp/data/buying_guide.txt"}),
        ]

        sources = format_sources(docs)

        self.assertEqual(
            sources,
            "Sources:\n- buying_guide.txt\n- maintenance_guide.txt",
        )

    def test_append_sources_keeps_answer_and_adds_sources(self):
        docs = [Document(page_content="A", metadata={"source": "data/troubleshooting_guide.txt"})]

        answer = append_sources("Wipe the charging contacts.", docs)

        self.assertEqual(
            answer,
            "Wipe the charging contacts.\n\nSources:\n- troubleshooting_guide.txt",
        )


if __name__ == "__main__":
    unittest.main()
