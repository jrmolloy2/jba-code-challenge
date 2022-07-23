import os

ROOT_PATH = os.path.dirname(__file__)
RESOURCES = os.path.join(ROOT_PATH, "resources")
TEST_FILE = [os.path.join(RESOURCES, file) for file in os.listdir(RESOURCES) if file.endswith(".pre")][0]
