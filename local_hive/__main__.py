from local_hive.service import LocalHiveService
from ovos_utils import wait_for_exit_signal

if __name__ == "__main__":
    localmind = LocalHiveService()
    localmind.start()
    wait_for_exit_signal()

