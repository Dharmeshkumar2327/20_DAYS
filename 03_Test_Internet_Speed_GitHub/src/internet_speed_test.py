"""Test internet download speed, upload speed, and ping."""

import speedtest


def test_speed():
    """Run a speed test and return download, upload, and ping values."""
    st = speedtest.Speedtest()

    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000

    st.get_servers([])
    ping = st.results.ping

    return round(download, 3), round(upload, 3), ping


def main():
    print("Testing internet speed... Please wait.\n")

    try:
        download, upload, ping = test_speed()
        print(f"Your ⏬ Download speed is {download} Mbps")
        print(f"Your ⏫ Upload speed is {upload} Mbps")
        print(f"Your Ping is {ping} ms")
    except Exception as error:
        print(f"Speed test failed: {error}")


if __name__ == "__main__":
    main()
