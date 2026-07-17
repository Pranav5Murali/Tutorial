#!/usr/bin/env python3

import subprocess
import shutil
import pymysql


def run_cmd(cmd):
    base_cmd = cmd.split()[0]

    if shutil.which(base_cmd) is None:
        return "[ERROR] Command '%s' not found." % base_cmd

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "[FAIL] Exit %d: %s" % (
            result.returncode,
            result.stderr.strip()
        )


def save_to_db(hostname, report):
    try:
        conn = pymysql.connect(
            host="172.17.0.4",
            port=3306,
            user="root",
            password="Password123",
            database="healthdb"
        )

        cursor = conn.cursor()

        sql = """
        INSERT INTO system_health
        (hostname, collected_time, report)
        VALUES (%s, NOW(), %s)
        """

        cursor.execute(sql, (hostname, report))

        conn.commit()

        cursor.close()
        conn.close()

        print("[OK] Health data saved to MariaDB")

    except Exception as e:
        print("[DB ERROR]", e)


def main():

    report = ""

    hostname = run_cmd("hostname")
    username = run_cmd("whoami")
    timestamp = run_cmd("date")

    report += "REMOTE SYSTEM HEALTH REPORT\n"
    report += "Hostname : " + hostname + "\n"
    report += "User     : " + username + "\n"
    report += "Time     : " + timestamp + "\n"


    report += "\n1. KERNEL & OS\n"
    report += run_cmd("uname -a")


    report += "\n\n2. MEMORY USAGE\n"
    report += run_cmd("free -h")


    report += "\n\n3. DISK SPACE\n"
    report += run_cmd("df -h /")


    report += "\n\n4. LOAD AVERAGE & UPTIME\n"
    report += run_cmd("uptime")


    report += "\n\n5. TOP 5 CPU PROCESSES\n"
    report += run_cmd("ps aux | sort -k3 -nr | head -6")


    report += "\n\n6. TOP 5 MEMORY PROCESSES\n"
    report += run_cmd("ps aux | sort -k4 -nr | head -6")


    save_to_db(hostname, report)


if __name__ == "__main__":
    main()
