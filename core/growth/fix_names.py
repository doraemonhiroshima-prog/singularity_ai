# core/growth/fix_names.py

import os
import re

from datetime import datetime


class FixNames:

    def __init__(self):

        self.log_file = (
            "fix_system_date.txt"
        )

    # =====================================================
    # SHOULD RUN
    # =====================================================
    def should_run(

        self,
        days=21
    ):

        if not os.path.exists(
            self.log_file
        ):

            return True

        try:

            with open(
                self.log_file,
                "r"
            ) as f:

                last = f.read().strip()

            last_date = datetime.strptime(
                last,
                "%Y-%m-%d"
            )

            diff = (
                datetime.now() - last_date
            ).days

            return diff >= days

        except:

            return True

    # =====================================================
    # SAVE DATE
    # =====================================================
    def save_date(self):

        with open(
            self.log_file,
            "w"
        ) as f:

            f.write(

                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )

    # =====================================================
    # CLEAN LINE
    # =====================================================
    def clean_line(

        self,
        line
    ):

        # コメント削除
        if "#" in line:

            line = (
                line.split("#")[0]
            )

        # ゴミ文字除去
        if re.search(
            r"[�]{2,}",
            line
        ):

            return ""

        return line

    # =====================================================
    # PROCESS FILE
    # =====================================================
    def process_file(

        self,
        filepath
    ):

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                lines = f.readlines()

            new_lines = []

            for line in lines:

                cleaned = (
                    self.clean_line(line)
                )

                if cleaned.strip() != "":

                    new_lines.append(
                        cleaned + "\n"
                    )

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as f:

                f.writelines(new_lines)

            print(
                f"✔ FIXED: {filepath}"
            )

        except Exception as e:

            print(
                f"❌ ERROR: {filepath} -> {e}"
            )

    # =====================================================
    # FIX CODE
    # =====================================================
    def fix_code(self):

        for root, dirs, files in os.walk("."):

            for file in files:

                if file.endswith(".py"):

                    self.process_file(

                        os.path.join(
                            root,
                            file
                        )
                    )

    # =====================================================
    # REPAIR NAMES
    # =====================================================
    def repair_names(self):

        print(
            "🔧 STOCK NAME REPAIR"
        )

    # =====================================================
    # UPDATE STOCK LIST
    # =====================================================
    def update_stock_list(self):

        print(
            "🔄 STOCK LIST UPDATE"
        )

    # =====================================================
    # RUN
    # =====================================================
    def run(

        self,

        fix_code=True,

        repair_names=True,

        update_stock_list=True,

        auto_interval=True
    ):

        # =============================================
        # INTERVAL CHECK
        # =============================================
        if auto_interval:

            if not self.should_run():

                print(
                    "SKIP FIX SYSTEM"
                )

                return

        # =============================================
        # FIX CODE
        # =============================================
        if fix_code:

            self.fix_code()

        # =============================================
        # REPAIR NAMES
        # =============================================
        if repair_names:

            self.repair_names()

        # =============================================
        # UPDATE STOCK LIST
        # =============================================
        if update_stock_list:

            self.update_stock_list()

        # =============================================
        # SAVE DATE
        # =============================================
        self.save_date()

        print(
            "✅ FIX SYSTEM DONE"
        )