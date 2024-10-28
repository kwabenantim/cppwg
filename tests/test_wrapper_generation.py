import os
import shutil
import subprocess
import unittest
from difflib import context_diff
from glob import glob


def file_diff(file_a: str, file_b: str) -> bool:
    """Check if two files have the same content.

    Parameters
    __________
    file_a: str
        The path to the first file
    file__b: str
        The path to the second file

    Returns
    __________
    str
        A diff of the two files
    """
    # Read files and remove excess whitespace
    with open(file_a, "r") as fa:
        a = [line.strip() for line in fa]
        a = [line for line in a if line]

    with open(file_b, "r") as fb:
        b = [line.strip() for line in fb]
        b = [line for line in b if line]

    return "\n".join(context_diff(a, b))


class TestWrapperGeneration(unittest.TestCase):
    def setUp(self) -> None:
        # Set paths to the shapes code, reference and generated wrappers, etc.
        root = os.path.abspath("examples/shapes")
        extern = os.path.join(root, "extern")
        self.src = os.path.join(root, "src/cpp")

        self.includes = glob(self.src + "/*/") + glob(extern + "/*/")

        self.wrapper = os.path.join(root, "wrapper")
        self.wrapper_gen = os.path.join(root, "wrapper.gen")

        self.config = os.path.join(self.wrapper, "package_info.yaml")
        self.script = os.path.abspath("cppwg/__main__.py")

    def test_wrapper_generation(self) -> None:
        """
        Generate wrappers and compare with the reference wrappers.
        """
        self.assertTrue(os.path.isdir(self.src), self.src)
        self.assertTrue(os.path.isdir(self.wrapper), self.wrapper)
        self.assertTrue(os.path.isfile(self.config), self.config)

        # Generate the wrappers
        subprocess.call(
            [
                "python",
                self.script,
                self.src,
                "--wrapper_root",
                self.wrapper_gen,
                "--package_info",
                self.config,
                "--includes",
            ]
            + self.includes
        )

        self.assertTrue(os.path.isdir(self.wrapper_gen), self.wrapper_gen)

        # Compare the generated files with reference files
        self.maxDiff = None
        for dirpath, _, filenames in os.walk(self.wrapper):
            for filename in filenames:
                if filename.endswith(".cppwg.cpp") or filename.endswith(".cppwg.hpp"):
                    file_ref = os.path.join(dirpath, filename)
                    file_gen = file_ref.replace(self.wrapper, self.wrapper_gen, 1)

                    self.assertTrue(os.path.isfile(file_ref), file_ref)
                    self.assertTrue(os.path.isfile(file_gen), file_gen)
                    self.assertEqual(file_diff(file_gen, file_ref), "", f"\n{file_ref}")

    def tearDown(self) -> None:
        shutil.rmtree(self.wrapper_gen)


if __name__ == "__main__":
    unittest.main()
