import unittest

from src.manager import DEFAULT_PROMPTS_DIR, filter_prompts, load_all_prompts, validate_repository


class ManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts = load_all_prompts(DEFAULT_PROMPTS_DIR)

    def test_repository_prompts_are_valid(self):
        self.assertEqual(validate_repository(DEFAULT_PROMPTS_DIR), {})

    def test_initial_library_has_every_category(self):
        categories = {prompt.category for prompt in self.prompts}
        self.assertEqual(
            categories,
            {"programming", "creative-writing", "visual-art", "audio-music", "productivity"},
        )

    def test_search_matches_title_tags_and_content(self):
        matches = filter_prompts(self.prompts, "Python")
        self.assertTrue(any(prompt.path == "programming/python-refactor.md" for prompt in matches))

    def test_category_filter(self):
        matches = filter_prompts(self.prompts, category="visual-art")
        self.assertTrue(matches)
        self.assertTrue(all(prompt.category == "visual-art" for prompt in matches))


if __name__ == "__main__":
    unittest.main()
