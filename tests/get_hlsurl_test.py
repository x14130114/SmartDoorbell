import boto3
import unittest

"""
Test class for retrieving the HLS URL from the active Amazon Kinesis Video Stream
Returns null if the stream is inactive

"""

class TestHLSUrl(unittest.TestCase):

    def test_hls_url(self):
        STREAM_NAME = "test"
        kvs = boto3.client("kinesisvideo")

        # Grab the endpoint from GetDataEndpoint
        endpoint = kvs.get_data_endpoint(
            APIName="GET_HLS_STREAMING_SESSION_URL",
            StreamName=STREAM_NAME
        )['DataEndpoint']

        # Grab the HLS Stream URL from the endpoint
        kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
        url = kvam.get_hls_streaming_session_url(
            StreamName=STREAM_NAME,
            PlaybackMode="LIVE"
        )['HLSStreamingSessionURL']


        # Print the HLS URL retrieved
        print(url)

if __name__ == '__main__':
    unittest.main()
