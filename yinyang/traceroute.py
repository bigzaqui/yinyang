from constants import ATLAS_API_KEY
from datetime import datetime
from ripe.atlas.cousteau import (
    Traceroute,
    AtlasSource,
    AtlasCreateRequest, AtlasStream)
import requests.packages.urllib3
import Queue
from ripe.atlas.sagan import TracerouteResult
requests.packages.urllib3.disable_warnings()

atlas_stream = AtlasStream()
q = Queue.Queue()


def run_traceroute(probe_id,destination_ip):
    global q
    traceroute = Traceroute(
        af=4,
        target=destination_ip,
        description="testing",
        protocol="ICMP",
    )

    source = AtlasSource(type="probes", value=probe_id, requested=1)

    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=ATLAS_API_KEY,
        measurements=[traceroute],
        sources=[source],
        is_oneoff=True
    )

    (is_success, response) = atlas_request.create()
    print response

    if not is_success:
        raise Exception('Error creating the measurement.')
    __fetch_result(response['measurements'][0])
    return q.get()


def __on_result_response(*args):
    global atlas_stream
    global q
    q.put(TracerouteResult(args[0]))
    atlas_stream.disconnect()


def __fetch_result(response):

    global atlas_stream
    atlas_stream.connect()
    # Measurement results
    stream_type = "result"
    # Bind function we want to run with every result message received
    atlas_stream.bind_stream(stream_type, __on_result_response)
    # Subscribe to new stream for 1001 measurement results
    stream_parameters = {"msm": response}
    print "measurement: %s" % response
    atlas_stream.start_stream(stream_type=stream_type, **stream_parameters)

    # Timeout all subscriptions after 5 secs. Leave seconds empty for no timeout.
    # Make sure you have this line after you start *all* your streams
    atlas_stream.timeout(seconds=200)
    if q.empty():
        raise Exception('Streamer timed out before fetching the result.')



