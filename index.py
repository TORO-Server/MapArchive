import logging
import re
import os
import shutil


def genLogger(name: str):
    logger = logging.getLogger(name)
    # コンソールに出力するためのハンドラーを作成
    console_handler = logging.StreamHandler()

    logger.setLevel(logging.DEBUG)  # ロガー全体のログレベル設定
    console_handler.setLevel(logging.DEBUG)  # ハンドラーのログレベルを設定

    # フォーマッターを作成
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    # ロガーにハンドラーを追加
    logger.addHandler(console_handler)

    return logger


class move_files:
    def __init__(self, filter: re.Pattern, source_dir=os.getcwd()):
        self.filter = filter
        self.source_dir = source_dir
        self.logger = genLogger("MoveFiles")

    def start(self):
        for filename in os.listdir(self.source_dir):
            self.move_file_manager(filename)

    def getTargetDir(self, filename: str) -> str:

        if not re.search(self.filter, filename):
            return None

        fileNameList = filename.split("-")
        if len(fileNameList) != 5:
            return None

        return os.path.join(
            self.source_dir,
            fileNameList[0],
            fileNameList[2].zfill(4),
            fileNameList[3].zfill(2)
        )

    def move_file(self, filename: str, target_dir: str):
        file_path_from = os.path.join(self.source_dir, filename)
        file_path_to = os.path.join(target_dir, filename)

        # ディレクトリが存在しない場合は作成
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            self.logger.info(f"Create Directory: {target_dir}")

        try:
            if os.path.isfile(file_path_from):
                shutil.move(file_path_from, file_path_to)
                self.logger.info(f"Move {file_path_from} to {file_path_to}")
        except Exception as e:
            self.logger.error(e)

    def move_file_manager(self,  filename: str):

        target_dir = self.getTargetDir(filename)

        if not target_dir:
            return

        self.move_file(filename, target_dir)


if __name__ == "__main__":
    move_files(r".*\.png").start()
