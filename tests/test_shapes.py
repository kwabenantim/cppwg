import os
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


class TestShapes(unittest.TestCase):

    def test_wrapper_generation(self) -> None:
        """
        Generate wrappers and compare with the reference wrappers.
        """

        # Set paths to the shapes code, reference and generated wrappers, etc.
        shapes_root = os.path.abspath("examples/shapes")
        shapes_src = os.path.join(shapes_root, "src")
        extern_src = os.path.join(shapes_root, "extern")

        wrapper_root_ref = os.path.join(shapes_root, "wrapper")
        wrapper_root_gen = os.path.join(shapes_root, "gen_wrapper")

        self.assertTrue(os.path.isdir(shapes_root))
        self.assertTrue(os.path.isdir(shapes_src))
        self.assertTrue(os.path.isdir(extern_src))
        self.assertTrue(os.path.isdir(wrapper_root_ref))

        generate_script = os.path.abspath("cppwg/__main__.py")
        package_info_path = os.path.join(wrapper_root_ref, "package_info.yaml")
        self.assertTrue(os.path.isfile(package_info_path))

        includes = glob(shapes_src + "/*/") + glob(extern_src + "/*/")

        # Generate the wrappers
        subprocess.call(
            [
                "python",
                generate_script,
                shapes_src,
                "--wrapper_root",
                wrapper_root_gen,
                "--package_info",
                package_info_path,
                "--includes",
            ]
            + includes
        )

        self.assertTrue(os.path.isdir(wrapper_root_gen))

        # Compare the generated files with reference files
        self.maxDiff = None
        for dirpath, _, filenames in os.walk(wrapper_root_ref):
            for filename in filenames:
                if filename.endswith(".cppwg.cpp") or filename.endswith(".cppwg.hpp"):
                    file_ref = os.path.join(dirpath, filename)
                    file_gen = file_ref.replace(wrapper_root_ref, wrapper_root_gen, 1)

                    self.assertTrue(os.path.isfile(file_ref))
                    self.assertTrue(os.path.isfile(file_gen))
                    self.assertEqual(file_diff(file_gen, file_ref), "", f"\n{file_ref}")


if __name__ == "__main__":
    unittest.main()
